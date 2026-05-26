# Confluence REST API Reference

## Authentication

**CRITICAL**: Adobe Wiki requires Bearer token authentication (NOT basic auth).

All API calls MUST use:
```bash
curl -H "Authorization: Bearer $WIKI_TOKEN" -H "Accept: application/json" "https://wiki.corp.adobe.com/rest/api/..."
```

**Environment Variables:**
- `WIKI_TOKEN`: Personal access token from https://wiki.corp.adobe.com/plugins/personalaccesstokens/usertokens.action
- **VPN Required**: Both read and write operations require Adobe VPN connection

### Critical: Bash Tool Usage for API Calls

**⚠️ SHELL VARIABLE SUBSTITUTION REQUIREMENT ⚠️**

When using the Bash tool to make API calls, you MUST allow shell variable substitution to occur.

**✅ CORRECT - Let the shell substitute variables:**
```bash
curl -H "Authorization: Bearer $WIKI_TOKEN" "https://wiki.corp.adobe.com/rest/api/content/PAGE_ID"
```

**❌ INCORRECT - Using -s flag or piping can cause auth failures:**
```bash
# These may fail intermittently due to timing/buffering issues
curl -s -H "Authorization: Bearer $WIKI_TOKEN" "..." | python3 -m json.tool
curl -H "Authorization: Bearer $WIKI_TOKEN" "..." | jq
```

**Best Practices:**
1. **Simple curl commands work best** - Let output display naturally, parse later if needed
2. **Avoid piping during authentication testing** - First verify API call works, then add formatting
3. **Test authentication first** - Verify token with a simple API call before complex operations
4. **Single Bash invocation** - Keep entire API call in one Bash tool call without preprocessing

**Why This Matters:**
- The Bash tool executes in a shell session that sources `~/.zshrc` where tokens are defined
- Piping or complex command chaining can cause timing issues with variable substitution
- Some curl flags (like `-s`) combined with piping can interfere with proper token passing

## Common API Endpoints

### Get Page by ID
```bash
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/content/PAGE_ID?expand=body.storage,version"
```

### Get Page by Title
```bash
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/content?spaceKey=GenStudio&title=PAGE_TITLE&expand=body.storage,version"
```

### Get Page from URL or Page ID

**Use the script** (recommended):
```bash
python3 scripts/wiki_get_page.py [--url URL | --page-id PAGE_ID] [--format {json,html,summary}]
```

**Input options** (choose one):
- `--url URL` - Confluence page URL
- `--page-id PAGE_ID` - Direct page ID

**Output formats**:
- `--format summary` - Human-readable with metadata and content preview (default)
- `--format json` - Full API response as JSON
- `--format html` - Raw Confluence storage format (XHTML)

**Examples**:
```bash
# Fetch by URL (most common)
python3 scripts/wiki_get_page.py --url "https://wiki.corp.adobe.com/display/GenStudio/Page+Title"

# Fetch by page ID
python3 scripts/wiki_get_page.py --page-id 3647578884

# Get JSON output
python3 scripts/wiki_get_page.py --url "..." --format json

# Get HTML content only
python3 scripts/wiki_get_page.py --url "..." --format html

# Extract specific JSON field with jq
python3 scripts/wiki_get_page.py --page-id 3647578884 --format json 2>/dev/null | jq -r '.title'
```

**How it works**: The script fetches the HTML, extracts the page ID from the `ajs-page-id` meta tag, and retrieves the full content. This is deterministic and reliable.

### Search Content
```bash
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/search?cql=type=page+AND+space=GenStudio+AND+title~\"search+term\""
```

### Create New Page
```bash
curl -X POST -H "Authorization: Bearer $WIKI_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "type": "page",
    "title": "Page Title",
    "ancestors": [{"id": "PARENT_PAGE_ID"}],
    "space": {"key": "GenStudio"},
    "body": {
      "storage": {
        "value": "<h2>Content</h2><p>Page content...</p>",
        "representation": "storage"
      }
    }
  }' \
  "https://wiki.corp.adobe.com/rest/api/content"
```

### Update Existing Page
```bash
curl -X PUT -H "Authorization: Bearer $WIKI_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "id": "PAGE_ID",
    "type": "page",
    "title": "Page Title",
    "space": {"key": "GenStudio"},
    "version": {"number": INCREMENTED_VERSION},
    "body": {
      "storage": {
        "value": "<h2>Updated Content</h2>",
        "representation": "storage"
      }
    }
  }' \
  "https://wiki.corp.adobe.com/rest/api/content/PAGE_ID"
```

**Important**: Must increment version number with each update.

### List Child Pages
```bash
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/content/PARENT_PAGE_ID/child/page?limit=100"
```

### List Attachments
```bash
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/content/PAGE_ID/child/attachment"
```

### Upload Attachment
```bash
curl -X POST \
  -H "Authorization: Bearer $WIKI_TOKEN" \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/file;filename=Display-Name" \
  -F "minorEdit=false" \
  -F "comment=File description" \
  "https://wiki.corp.adobe.com/rest/api/content/PAGE_ID/child/attachment"
```

**Critical for draw.io diagrams**: Filename must NOT have extension.

### Download Attachment
```bash
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "ATTACHMENT_DOWNLOAD_URL" -o output-file.ext
```

## JSON Parsing Best Practices

**NEVER use `python3 -c` for JSON parsing** - it fails with nested quotes and complex JSON.

**✅ Recommended: Use jq or save to file first**
```bash
# Option 1: Use jq
curl -s -H "Authorization: Bearer $WIKI_TOKEN" "..." | jq -r '.version.number'

# Option 2: Save to file, then parse with Python script
curl -s -H "Authorization: Bearer $WIKI_TOKEN" "..." > /tmp/response.json
python3 parse_script.py /tmp/response.json
```

## Error Handling

### Common Errors

**"Version conflict"**: Page modified since last read. Fetch latest version and retry.

**"Error parsing xhtml"**: Content has unescaped HTML entities. Use `html_escape.py` script.

**"403 Forbidden" / "anonymous" user**: Authentication failed. Verify:
1. VPN connected
2. `$WIKI_TOKEN` is set: `echo ${#WIKI_TOKEN}`
3. Token not expired (get new one if needed)
4. Bearer keyword present: `Authorization: Bearer $WIKI_TOKEN`

**"Attachment not found"**: Filename mismatch (case-sensitive). For draw.io, ensure no file extension.

**"Macro not found"**: Check macro name spelling (`inc-drawio`, `plantuml`, `code`).

## Rate Limiting

Adobe's on-prem Confluence instance has rate limiting. If you encounter 429 errors:
- Wait 60 seconds before retrying
- Batch operations when possible
- Cache page content locally to minimize API calls
