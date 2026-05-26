#!/usr/bin/env python3
"""
Slack API Client - Shared module for Slack integration scripts

Provides:
- Token management (bot/user token selection)
- HTTP client (curl subprocess)
- Token fallback logic (user->bot or bot->user retry on auth/permission errors)
- Rate limiting with exponential backoff
- Error classification (6 error types)
- Response parsing and validation

Zero external dependencies: Python stdlib + curl only
"""

import os
import sys
import json
import subprocess
import time
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Error Classes (6 error types from MCP server)

class SlackError(Exception):
    """Base exception for Slack API errors."""
    pass


class SlackAuthenticationError(SlackError):
    """Invalid/expired token errors."""
    pass


class SlackPermissionError(SlackError):
    """Missing scope or permission errors."""
    pass


class SlackResourceNotFoundError(SlackError):
    """Channel/user/message not found errors."""
    pass


class SlackRateLimitError(SlackError):
    """Rate limit exceeded (includes retry_after)."""
    def __init__(self, message: str, retry_after: int):
        super().__init__(message)
        self.retry_after = retry_after


class SlackValidationError(SlackError):
    """Invalid parameter/argument errors."""
    pass


# Token Type Enum

class TokenType(Enum):
    """Token type for Slack API authentication."""
    BOT = "bot"
    USER = "user"


# Configuration

class SlackConfig:
    """Configuration loader for Slack API client."""

    def __init__(self):
        """Load configuration from environment variables."""
        self.bot_token = os.getenv('SLACK_BOT_TOKEN')
        self.user_token = os.getenv('SLACK_USER_TOKEN')
        self.team_id = os.getenv('SLACK_TEAM_ID')
        self.default_token = os.getenv('SLACK_DEFAULT_TOKEN', 'bot')
        self.api_base_url = os.getenv('SLACK_API_BASE_URL', 'https://slack.com/api')
        self.log_file = os.getenv('SLACK_LOG_FILE')

        self._validate()

    def _validate(self):
        """Validate configuration."""
        if not self.bot_token and not self.user_token:
            raise SlackError(
                "No tokens configured. Set SLACK_BOT_TOKEN or SLACK_USER_TOKEN environment variable.\n"
                "Get tokens at: https://api.slack.com/apps"
            )

        if self.default_token not in ['bot', 'user']:
            raise SlackError(f"Invalid SLACK_DEFAULT_TOKEN: {self.default_token}. Must be 'bot' or 'user'")

        if self.default_token == 'user' and not self.user_token:
            raise SlackError("SLACK_USER_TOKEN required when SLACK_DEFAULT_TOKEN='user'")

        if self.default_token == 'bot' and not self.bot_token:
            raise SlackError("SLACK_BOT_TOKEN required when SLACK_DEFAULT_TOKEN='bot'")


# HTTP Method Selection (GET vs POST)

# Slack API methods that should use GET (mirrors MCP server utils.ts)
GET_METHODS = {
    'search.messages',
    'conversations.list',
    'conversations.info',
    'conversations.history',
    'users.list',
    'users.info',
    'users.lookupByEmail',
    'conversations.replies',
    'usergroups.list',
    'usergroups.users.list',
}


# Error Classification Map

ERROR_MAP = {
    'invalid_auth': SlackAuthenticationError,
    'token_revoked': SlackAuthenticationError,
    'account_inactive': SlackAuthenticationError,
    'not_authed': SlackAuthenticationError,
    'missing_scope': SlackPermissionError,
    'not_allowed_token_type': SlackPermissionError,
    'forbidden': SlackPermissionError,
    'channel_not_found': SlackResourceNotFoundError,
    'user_not_found': SlackResourceNotFoundError,
    'message_not_found': SlackResourceNotFoundError,
    'thread_not_found': SlackResourceNotFoundError,
    'file_not_found': SlackResourceNotFoundError,
    'rate_limited': SlackRateLimitError,
    'invalid_arguments': SlackValidationError,
    'validation_error': SlackValidationError,
}


# Help Text by Error Type

ERROR_HELP = {
    SlackAuthenticationError: "Check token validity and expiration at https://api.slack.com/apps",
    SlackPermissionError: "Verify token has required scopes. Check app permissions.",
    SlackResourceNotFoundError: "Verify resource ID is correct and bot has access",
    SlackRateLimitError: "Rate limit exceeded. Retry after specified delay.",
    SlackValidationError: "Check parameter values and types",
}


# Main Client Class

class SlackAPIClient:
    """
    Slack API client with token fallback and error handling.

    Implements the same token fallback logic as MCP server:
    - Try primary token (user or bot based on preference)
    - If auth/permission error, try fallback token
    - Classify errors into appropriate types
    - Handle rate limiting with exponential backoff
    """

    def __init__(self, config: Optional[SlackConfig] = None):
        """
        Initialize Slack API client.

        Args:
            config: Optional SlackConfig instance (creates default if None)
        """
        self.config = config or SlackConfig()

    def request(self, method: str, params: Optional[Dict[str, Any]] = None,
                use_user_token: Optional[bool] = None,
                allow_fallback: bool = True) -> Dict[str, Any]:
        """
        Execute Slack API request with token fallback.

        Args:
            method: Slack API method (e.g., 'conversations.history')
            params: Request parameters
            use_user_token: Explicit token preference (None = auto-select)
            allow_fallback: Enable automatic token fallback on auth/permission errors

        Returns:
            Parsed JSON response from Slack API

        Raises:
            SlackError subclasses for various error conditions
        """
        params = params or {}

        # Determine primary token preference
        prefer_user_token = self._determine_token_preference(method, use_user_token)

        # Try primary token
        try:
            return self._make_request(method, params, prefer_user_token)
        except (SlackAuthenticationError, SlackPermissionError) as primary_error:
            if not allow_fallback:
                raise

            # Try fallback token
            primary_label = 'user' if prefer_user_token else 'bot'
            fallback_label = 'bot' if prefer_user_token else 'user'

            print(f"Token fallback: {primary_label}->{fallback_label} for {method}: {primary_error}",
                  file=sys.stderr)

            try:
                return self._make_request(method, params, not prefer_user_token)
            except Exception as fallback_error:
                raise SlackError(
                    f"Both tokens failed for {method}.\n"
                    f"Primary ({primary_label}): {primary_error}\n"
                    f"Fallback ({fallback_label}): {fallback_error}\n"
                    f"Check token configuration and required scopes."
                )

    def _determine_token_preference(self, method: str, use_user_token: Optional[bool]) -> bool:
        """
        Determine which token to use based on method and preferences.

        Args:
            method: Slack API method
            use_user_token: Explicit preference (overrides defaults)

        Returns:
            True to use user token, False to use bot token
        """
        # Explicit preference has highest priority
        if use_user_token is not None:
            return use_user_token

        # Method-specific requirements (search and conversations.open need user token)
        if method in ['search.messages', 'conversations.open']:
            return True

        # Default preference from config
        return self.config.default_token == 'user'

    def _make_request(self, method: str, params: Dict[str, Any],
                     use_user_token: bool, retry_attempt: int = 0) -> Dict[str, Any]:
        """
        Execute HTTP request to Slack API using curl.

        Args:
            method: Slack API method
            params: Request parameters
            use_user_token: Whether to use user token (vs bot token)
            retry_attempt: Current retry attempt number (for rate limiting)

        Returns:
            Parsed JSON response

        Raises:
            SlackError subclasses for various error conditions
        """
        # Select token
        if use_user_token:
            if not self.config.user_token:
                raise SlackAuthenticationError(
                    f"User token required for {method} but SLACK_USER_TOKEN is not configured"
                )
            token = self.config.user_token
            token_type = TokenType.USER
        else:
            if not self.config.bot_token:
                raise SlackAuthenticationError(
                    f"Bot token required for {method} but SLACK_BOT_TOKEN is not configured"
                )
            token = self.config.bot_token
            token_type = TokenType.BOT

        # Build URL and determine HTTP method
        url = f"{self.config.api_base_url}/{method}"
        http_method = 'GET' if method in GET_METHODS else 'POST'

        # Log request if logging enabled
        self._log_request(method, params, token_type, token)

        # Build curl command
        cmd = [
            'curl', '-s',
            '-w', '\n%{http_code}',  # Append HTTP status code
            '-X', http_method,
            '-H', f'Authorization: Bearer {token}',
        ]

        if http_method == 'GET':
            # Add parameters to URL as query string
            if params:
                query_params = []
                for key, value in params.items():
                    if value is not None:
                        query_params.append(f"{key}={self._urlencode(str(value))}")
                if query_params:
                    url += '?' + '&'.join(query_params)
            cmd.extend(['-H', 'Content-Type: application/x-www-form-urlencoded'])
        else:
            # POST with JSON body
            cmd.extend([
                '-H', 'Content-Type: application/json; charset=utf-8',
                '-d', json.dumps(params)
            ])

        cmd.append(url)

        # Execute curl subprocess
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            raise SlackError(f"Request to {method} timed out after 30 seconds")
        except Exception as e:
            raise SlackError(f"Failed to execute curl: {e}")

        if result.returncode != 0:
            raise SlackError(f"curl command failed: {result.stderr}")

        # Parse response (body + HTTP status code)
        output_lines = result.stdout.strip().split('\n')
        if len(output_lines) < 2:
            raise SlackError(f"Invalid curl response format: {result.stdout}")

        http_status = int(output_lines[-1])
        response_body = '\n'.join(output_lines[:-1])

        # Handle HTTP-level errors
        if http_status == 401:
            raise SlackAuthenticationError(
                f"Invalid authentication token for {method}. "
                f"{token_type.value.capitalize()} token may be expired or invalid."
            )
        elif http_status == 403:
            raise SlackPermissionError(
                f"Not authorized to perform {method}. "
                f"{token_type.value.capitalize()} token may lack required permissions."
            )
        elif http_status == 404:
            raise SlackResourceNotFoundError(f"Resource not found for {method}")
        elif http_status == 429:
            # Rate limit - extract Retry-After header if available
            retry_after = 60  # Default to 60 seconds
            # Note: curl -w doesn't give us headers easily, so we use default
            return self._handle_rate_limit(method, params, use_user_token, retry_after, retry_attempt)
        elif http_status >= 400:
            raise SlackError(f"HTTP error {http_status} for {method}: {response_body}")

        # Parse JSON response
        try:
            data = json.loads(response_body)
        except json.JSONDecodeError as e:
            raise SlackError(f"Failed to parse JSON response: {e}\nResponse: {response_body}")

        # Check for Slack API-level errors
        if not data.get('ok', False):
            error_code = data.get('error', 'unknown_error')
            self._raise_classified_error(error_code, method, data)

        return data

    def _handle_rate_limit(self, method: str, params: Dict[str, Any],
                          use_user_token: bool, retry_after: int, attempt: int) -> Dict[str, Any]:
        """
        Handle rate limit with exponential backoff.

        Args:
            method: Slack API method
            params: Request parameters
            use_user_token: Token preference
            retry_after: Seconds to wait from Retry-After header
            attempt: Current attempt number

        Returns:
            Response from retried request

        Raises:
            SlackRateLimitError if max retries exceeded
        """
        max_retries = 3

        if attempt >= max_retries:
            raise SlackRateLimitError(
                f"Rate limit exceeded for {method} after {max_retries} retries",
                retry_after
            )

        # Exponential backoff: 1s, 2s, 4s
        wait_time = min(retry_after, 2 ** attempt)
        print(f"Rate limited. Waiting {wait_time}s (attempt {attempt + 1}/{max_retries})...",
              file=sys.stderr)
        time.sleep(wait_time)

        # Retry request
        return self._make_request(method, params, use_user_token, attempt + 1)

    def _raise_classified_error(self, error_code: str, method: str, data: Dict[str, Any]):
        """
        Raise appropriate exception based on Slack error code.

        Args:
            error_code: Slack error code (e.g., 'channel_not_found')
            method: API method that failed
            data: Full response data from Slack

        Raises:
            Appropriate SlackError subclass
        """
        error_class = ERROR_MAP.get(error_code, SlackError)
        error_message = data.get('error', error_code)

        if error_class == SlackRateLimitError:
            # Special handling for rate limit errors
            retry_after = data.get('retry_after', 60)
            raise SlackRateLimitError(
                f"Rate limit exceeded for {method}: {error_message}",
                retry_after
            )
        else:
            help_text = ERROR_HELP.get(error_class, "Check Slack API documentation")
            raise error_class(
                f"{method} failed: {error_message}\nHelp: {help_text}"
            )

    def _urlencode(self, value: str) -> str:
        """
        URL encode a parameter value.

        Args:
            value: Value to encode

        Returns:
            URL-encoded string
        """
        # Simple URL encoding (enough for Slack API parameters)
        import urllib.parse
        return urllib.parse.quote(value, safe='')

    def _log_request(self, method: str, params: Dict[str, Any],
                    token_type: TokenType, token: str):
        """
        Log request details to log file (if configured).

        Args:
            method: Slack API method
            params: Request parameters
            token_type: Type of token being used
            token: The actual token (will be masked)
        """
        if not self.config.log_file:
            return

        try:
            log_file = os.path.expanduser(self.config.log_file)
            with open(log_file, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                masked_token = f"{token_type.value} ({token[:8]}***{token[-3:]})"
                f.write(f"[{timestamp}] [{method}] Token: {masked_token}\n")
                f.write(f"  Params: {json.dumps(params)}\n")
        except Exception as e:
            # Don't fail the request if logging fails
            print(f"Warning: Failed to write to log file: {e}", file=sys.stderr)


# Utility Functions

def format_error_output(error: Exception, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format error for JSON output to stderr.

    Args:
        error: Exception that occurred
        method: API method that failed
        params: Parameters used in request

    Returns:
        Error dictionary for JSON output
    """
    error_type = type(error).__name__
    error_code = None

    # Extract error code if it's a Slack error
    if isinstance(error, SlackError):
        error_message = str(error)
        # Try to extract error code from message
        if ':' in error_message:
            parts = error_message.split(':', 1)
            if 'failed' in parts[0]:
                error_code = parts[1].strip().split('\n')[0].strip()

    result = {
        'ok': False,
        'error_type': error_type,
        'message': str(error),
        'method': method,
        'timestamp': datetime.now().isoformat()
    }

    if error_code:
        result['error'] = error_code

    if isinstance(error, SlackRateLimitError):
        result['retry_after'] = error.retry_after

    help_text = ERROR_HELP.get(type(error))
    if help_text:
        result['help'] = help_text

    return result


def format_success_output(data: Dict[str, Any], execution_time_ms: Optional[int] = None) -> Dict[str, Any]:
    """
    Format successful response for JSON output to stdout.

    Args:
        data: Response data from Slack API
        execution_time_ms: Optional execution time in milliseconds

    Returns:
        Formatted success response
    """
    result = {
        'ok': True,
        'data': data
    }

    if execution_time_ms is not None:
        result['execution_time_ms'] = execution_time_ms

    return result
