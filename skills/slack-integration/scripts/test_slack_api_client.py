#!/usr/bin/env python3
"""
Test suite for Slack API client

Tests the shared slack_api_client module functionality.
"""

import sys
import os
import json
import subprocess
from typing import Dict, Any


def run_test(test_name: str, test_func):
    """Run a test and report results."""
    try:
        test_func()
        print(f"✓ {test_name}")
        return True
    except AssertionError as e:
        print(f"✗ {test_name}: {e}")
        return False
    except Exception as e:
        print(f"✗ {test_name}: Unexpected error: {e}")
        return False


def test_config_validation():
    """Test that SlackConfig validates environment variables."""
    # Save original env vars
    original_bot_token = os.environ.get('SLACK_BOT_TOKEN')
    original_user_token = os.environ.get('SLACK_USER_TOKEN')

    try:
        # Clear tokens to test validation
        if 'SLACK_BOT_TOKEN' in os.environ:
            del os.environ['SLACK_BOT_TOKEN']
        if 'SLACK_USER_TOKEN' in os.environ:
            del os.environ['SLACK_USER_TOKEN']

        # Import after clearing env vars
        from slack_api_client import SlackConfig, SlackError

        try:
            config = SlackConfig()
            raise AssertionError("Should have raised SlackError for missing tokens")
        except SlackError as e:
            assert "No tokens configured" in str(e), f"Wrong error message: {e}"

    finally:
        # Restore original env vars
        if original_bot_token:
            os.environ['SLACK_BOT_TOKEN'] = original_bot_token
        if original_user_token:
            os.environ['SLACK_USER_TOKEN'] = original_user_token


def test_error_classification():
    """Test that error codes are classified correctly."""
    from slack_api_client import ERROR_MAP, SlackAuthenticationError, SlackPermissionError
    from slack_api_client import SlackResourceNotFoundError, SlackRateLimitError, SlackValidationError

    # Test auth errors
    assert ERROR_MAP['invalid_auth'] == SlackAuthenticationError
    assert ERROR_MAP['token_revoked'] == SlackAuthenticationError

    # Test permission errors
    assert ERROR_MAP['missing_scope'] == SlackPermissionError
    assert ERROR_MAP['forbidden'] == SlackPermissionError

    # Test not found errors
    assert ERROR_MAP['channel_not_found'] == SlackResourceNotFoundError
    assert ERROR_MAP['user_not_found'] == SlackResourceNotFoundError

    # Test rate limit
    assert ERROR_MAP['rate_limited'] == SlackRateLimitError

    # Test validation errors
    assert ERROR_MAP['invalid_arguments'] == SlackValidationError


def test_get_methods():
    """Test that GET methods are correctly identified."""
    from slack_api_client import GET_METHODS

    # Methods that should use GET
    assert 'conversations.list' in GET_METHODS
    assert 'conversations.info' in GET_METHODS
    assert 'conversations.history' in GET_METHODS
    assert 'users.list' in GET_METHODS
    assert 'search.messages' in GET_METHODS

    # Methods that should use POST
    assert 'chat.postMessage' not in GET_METHODS
    assert 'reactions.add' not in GET_METHODS


def test_token_type_enum():
    """Test TokenType enum."""
    from slack_api_client import TokenType

    assert TokenType.BOT.value == "bot"
    assert TokenType.USER.value == "user"


def test_error_output_format():
    """Test error output formatting."""
    from slack_api_client import format_error_output, SlackAuthenticationError

    error = SlackAuthenticationError("Invalid token")
    output = format_error_output(error, 'conversations.list', {'channel': 'C123'})

    assert output['ok'] is False
    assert output['error_type'] == 'SlackAuthenticationError'
    assert 'Invalid token' in output['message']
    assert output['method'] == 'conversations.list'
    assert 'timestamp' in output
    assert 'help' in output


def test_success_output_format():
    """Test success output formatting."""
    from slack_api_client import format_success_output

    data = {'ok': True, 'channel': 'C123', 'messages': []}
    output = format_success_output(data, 123)

    assert output['ok'] is True
    assert output['data'] == data
    assert output['execution_time_ms'] == 123


def test_scripts_executable():
    """Test that all operation scripts are executable."""
    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    scripts = [
        'slack_list_channels.py',
        'slack_get_channel_info.py',
        'slack_get_channel_history.py',
        'slack_get_thread_replies.py',
        'slack_post_message.py',
        'slack_send_dm.py',
        'slack_send_group_dm.py',
        'slack_reply_to_thread.py',
        'slack_update_message.py',
        'slack_add_reaction.py',
        'slack_search_messages.py',
        'slack_get_users.py',
        'slack_get_user_profile.py',
        'slack_get_user_by_email.py',
        'slack_search_users.py',
        'slack_lookup_user.py',
        'slack_list_usergroups.py',
        'slack_get_usergroup_members.py',
    ]

    for script in scripts:
        script_path = os.path.join(scripts_dir, script)
        assert os.path.exists(script_path), f"Script {script} does not exist"
        assert os.access(script_path, os.X_OK), f"Script {script} is not executable"


def test_scripts_have_help():
    """Test that all operation scripts have --help option."""
    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    scripts = [
        'slack_list_channels.py',
        'slack_get_channel_info.py',
    ]

    for script in scripts:
        script_path = os.path.join(scripts_dir, script)
        result = subprocess.run([script_path, '--help'],
                              capture_output=True, text=True)
        assert result.returncode == 0, f"Script {script} --help failed"
        assert 'usage:' in result.stdout.lower(), f"Script {script} has no usage help"


def main():
    """Run all tests."""
    print("Running Slack API Client Tests\n")

    tests = [
        ("Config validation", test_config_validation),
        ("Error classification", test_error_classification),
        ("GET methods identification", test_get_methods),
        ("TokenType enum", test_token_type_enum),
        ("Error output format", test_error_output_format),
        ("Success output format", test_success_output_format),
        ("Scripts executable", test_scripts_executable),
        ("Scripts have help", test_scripts_have_help),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print(f"{'='*60}\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
