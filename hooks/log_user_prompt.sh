#!/bin/bash

# Script to log user prompts to .chat folder in the current project
# Usage: Called by Claude Code UserPromptSubmit hook

# Use current working directory (where Claude Code is running)
PROJECT_DIR="$(pwd)"

# Create .chat directory if it doesn't exist
CHAT_DIR="${PROJECT_DIR}/.chat"
mkdir -p "${CHAT_DIR}"

# Log file with date in filename
LOG_FILE="${CHAT_DIR}/prompts_$(date +%Y-%m-%d).log"

# Get current timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Read the JSON input from stdin and extract the prompt
INPUT=$(cat)
PROMPT=$(echo "${INPUT}" | jq -r '.prompt // empty' 2>/dev/null)

# If jq parsing fails or prompt is empty, use raw input
if [ -z "${PROMPT}" ]; then
    PROMPT="${INPUT}"
fi

# Log the prompt with timestamp
echo "===========" >> "${LOG_FILE}"
echo "[${TIMESTAMP}]" >> "${LOG_FILE}"
echo "${PROMPT}" >> "${LOG_FILE}"
echo "" >> "${LOG_FILE}"

# Also keep a combined log of all prompts
ALL_PROMPTS_LOG="${CHAT_DIR}/all_prompts.log"
echo "===========" >> "${ALL_PROMPTS_LOG}"
echo "[${TIMESTAMP}]" >> "${ALL_PROMPTS_LOG}"
echo "${PROMPT}" >> "${ALL_PROMPTS_LOG}"
echo "" >> "${ALL_PROMPTS_LOG}"
