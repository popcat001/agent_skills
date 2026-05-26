---
name: confluence-wiki
description: This skill should be used when working with Adobe's on-prem Confluence wiki, including creating or updating technical documentation, generating diagrams (draw.io, PlantUML), managing wiki pages in the GenStudio Engineering workspace, or linking documentation to Jira tickets. Use when the user mentions wiki, Confluence, documentation, diagrams, architectural proposals, or needs to create/update wiki pages.
---

# Confluence Wiki Documentation

## Overview

This skill provides comprehensive capabilities for creating and managing technical documentation in Adobe's on-prem Confluence wiki (wiki.corp.adobe.com). Handle wiki page creation, updates, diagram generation (draw.io and PlantUML), proper HTML escaping, index page curation, and Jira integration.

## Tool Selection for Wiki Operations

**CRITICAL**: Use the correct tool for each operation to preserve markup and avoid data loss.

| Operation | Correct Tool | Why |
|-----------|--------------|-----|
| **Create new page content** | Write | Creates fresh content for new pages |
| **Update existing page** | Edit | Preserves inline comments and markup |
| **Modify page section** | Edit | Surgical changes, keeps everything else intact |
| **Create diagram files** | Write | New files (`.drawio`, `.plantuml`) |

**Key Rule**: For ANY existing wiki page update, ALWAYS use **Edit tool**, NEVER Write tool.

## Core Capabilities

### 0. Reading Wiki Pages

Fetch existing wiki page content from a URL or page ID.

**Script**: `scripts/wiki_get_page.py` - Retrieves page content with automatic URL parsing

**Usage**:
```bash
# From URL (most common)
python3 scripts/wiki_get_page.py --url "https://wiki.corp.adobe.com/display/GenStudio/Page+Title"

# From page ID
python3 scripts/wiki_get_page.py --page-id 3647578884

# Output formats
python3 scripts/wiki_get_page.py --url "..." --format summary  # Human-readable (default)
python3 scripts/wiki_get_page.py --url "..." --format json     # Full JSON response
python3 scripts/wiki_get_page.py --url "..." --format html     # Raw HTML content
```

**Quick Start: I Have a URL**
1. Copy the wiki URL from your browser address bar
2. Run: `python3 scripts/wiki_get_page.py --url "YOUR_URL"`
3. Content is fetched and displayed

**How it works**:
- Fetches the HTML page from the display URL
- Extracts page ID from the `ajs-page-id` meta tag
- Fetches full page content via REST API using the page ID
- This approach is deterministic and doesn't rely on search

**Token validation**: Script automatically validates `WIKI_TOKEN` before making API calls

### 0.5. Searching Wiki Pages

**CRITICAL**: Use the correct search endpoint to avoid 403 errors.

**Correct endpoint**: `/rest/api/search` (NOT `/rest/api/content/search`)

**Why this matters**: In Confluence Data Center/Server (pre-7.x versions), the `/rest/api/content/search` endpoint has stricter permissions and doesn't properly respect Personal Access Tokens. The `/rest/api/search` endpoint works correctly.

**Usage**:
```bash
# Search by text (CQL query)
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/search?cql=text~'search+term'&limit=10"

# Search within specific space
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/search?cql=space=GenStudio+AND+text~'architecture'&limit=10"

# Search by title
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/search?cql=title~'Page+Title'&limit=10"

# Complex query
curl -H "Authorization: Bearer $WIKI_TOKEN" \
  "https://wiki.corp.adobe.com/rest/api/search?cql=space=GenStudio+AND+(text~'agent'+OR+title~'agent')&limit=10"
```

**Response structure**:
```json
{
  "results": [
    {
      "content": {
        "id": "3678252350",
        "type": "page",
        "title": "Page Title"
      },
      "url": "/display/Space/Page+Title",
      "excerpt": "...highlighted search terms..."
    }
  ],
  "totalSize": 123,
  "cqlQuery": "text~'search term'"
}
```

**Common CQL patterns**:
- `text~'keyword'` - Full-text search
- `title~'keyword'` - Search in titles only
- `space=SpaceKey` - Filter by space
- `type=page` - Filter by content type
- `AND`, `OR` - Combine conditions
- Use `+` for spaces in URLs

**Error troubleshooting**:
- **403 Forbidden with "Not permitted to use confluence"**: You're using wrong endpoint (`/rest/api/content/search` instead of `/rest/api/search`)
- **Empty results**: Search term doesn't exist or wrong space specified
- **Invalid CQL**: Check syntax (spaces must be `+`, proper operators)

**Reference**: See `references/confluence_api.md` for complete CQL syntax guide

### 1. Wiki Page Creation
Create new wiki pages under appropriate parent pages in the GenStudio Engineering workspace.

**Default parent page**: Engineering Proposals (ID: `3137163046`)

**Script**: `scripts/wiki_create_page.py` - Creates or updates pages with automatic token validation

**Usage**:
```bash
# Create new page
python3 scripts/wiki_create_page.py --title "Page Title" --space "GenStudio" --parent 3137163046 --file content.html

# Update existing page
python3 scripts/wiki_create_page.py --update 3650098139 --version 2 --file content.html
```

**Key principles**:
- Search first using `/search-work` to avoid duplicates
- Choose appropriate parent page based on content type
- Use Confluence storage format (XHTML + `ac:` macros)
- Escape HTML entities properly using `scripts/html_escape.py`
- Update index pages after creation (MANDATORY)

**Token validation**: Script automatically validates `WIKI_TOKEN` before making API calls

**Reference**: `references/confluence_api.md` for REST API endpoints

### 2. Diagram Creation

#### Draw.io Architecture Diagrams
Generate mxfile XML for architecture diagrams, data flow diagrams, and system designs.

**Process**:
1. Create `.drawio` file with mxfile XML using patterns from `references/diagram_styles.md`
2. Use color schemes: Green (processes), Blue (data), Yellow (decisions), Red (errors)
3. Upload as attachment using `scripts/wiki_attach_file.py --page-id <id> --file diagram.drawio`
4. Embed using `drawio` macro with `diagramName` parameter referencing the attachment

**Template**: `assets/drawio_template.xml` provides starting structure

**IMPORTANT**: Draw.io diagrams MUST be uploaded as attachments (`.drawio` extension), not embedded inline

#### PlantUML Sequence Diagrams
Generate PlantUML for sequence diagrams, flow diagrams, and interaction patterns.

**Process**:
1. Write PlantUML syntax (see `references/diagram_styles.md`)
2. Validate using `scripts/validate_plantuml.py` before submission
3. Embed directly in page using `plantuml` macro

**Common pitfalls**:
- Multi-line arrow labels (NOT supported - must be inline)
- Unclosed blocks (always use `end`)
- Invalid participant names

**Template**: `assets/plantuml_sequence_template.txt` provides examples

### 2.5. Diagram Validation Workflow

**CRITICAL**: Always validate and preview diagrams locally before uploading to Confluence.

#### PlantUML Validation

Validate syntax and generate preview images:

```bash
python3 scripts/render_plantuml.py \
  --input my-sequence.plantuml \
  --output-dir /tmp/previews/

# Inspect the generated PNG
open /tmp/previews/my-sequence.png
```

**Validation checks**:
- PlantUML syntax correctness (`-checksyntax`)
- Successful PNG rendering
- Line-by-line error reporting with context

**Output formats**:
- Human-readable (default): Status, errors, warnings, preview path
- JSON (`--json`): Machine-readable for automation

**Example output**:
```json
{
  "status": "success",
  "syntax_valid": true,
  "rendering_success": true,
  "preview_path": "/tmp/previews/diagram.png",
  "errors": [],
  "warnings": []
}
```

#### Draw.io Validation

Validate XML and generate preview images:

```bash
python3 scripts/render_drawio.py \
  --input architecture.drawio \
  --output-dir /tmp/previews/ \
  --format png

# Inspect the generated PNG
open /tmp/previews/architecture.png
```

**Tool detection**:
- Prefers `drawio-exporter` (Cargo) if available
- Falls back to Docker (`rlespinasse/drawio-export`)
- Provides installation instructions if neither available

**Validation checks**:
- XML well-formedness
- Required draw.io elements present (`<mxfile>`, `<diagram>`)
- Successful image rendering
- Layout issue detection

**Installation**:
```bash
# Option A: Cargo (requires Rust edition 2024+)
cargo install drawio-exporter

# Option B: Docker (requires Docker daemon running)
docker pull rlespinasse/drawio-export
```

#### Validation Workflow

**Recommended workflow for all diagrams**:

1. **Create** diagram content (PlantUML text or draw.io XML)
2. **Validate** locally using render scripts
   - PlantUML: `render_plantuml.py`
   - Draw.io: `render_drawio.py`
3. **Inspect** preview images for visual issues
   - Layout problems (overlapping boxes, misaligned arrows)
   - Text rendering issues (truncated labels, missing text)
   - Color scheme consistency
4. **Fix** any rendering errors or layout problems
5. **Re-validate** until clean
6. **Upload** to Confluence using `wiki_attach_file.py` (draw.io) or embed directly (PlantUML)

**Why validate locally?**
- Catch syntax errors before Confluence upload
- Verify visual layout matches expectations
- Avoid iterative fix-upload-check cycles on wiki
- Faster feedback loop during diagram development

**Reference**: `references/installation.md` for complete tool installation guide

### PlantUML Best Practices

**CRITICAL**: Never use inline `\n` escape sequences in note blocks.

#### Common Mistake: Inline Newlines

This causes "cannot create group" errors in Confluence:

```plantuml
note right: Item 1\nItem 2\nItem 3
```

Use multi-line blocks instead:

```plantuml
note right
Item 1
Item 2
Item 3
end note
```

**Full guide**: See `references/plantuml-best-practices.md` for complete syntax patterns, common issues, and troubleshooting.

## Draw.io Layout Best Practices

**CRITICAL**: Lines must never cut through boxes in technical diagrams.

### Pre-Upload Checklist
Before uploading any draw.io diagram to Confluence:
- [ ] Render diagram to PNG using Docker validation
- [ ] Visually inspect for lines cutting through boxes
- [ ] Check all labels are fully visible and well-positioned
- [ ] Verify adequate spacing between elements (min 20px)
- [ ] Confirm professional, uncluttered appearance

### Common Issues and Fixes

**Lines cutting through boxes**:
- Root cause: Using direct routing without waypoints
- Fix: Add `<Array as="points">` with waypoints to route around obstacles
- See: `references/drawio-layout-best-practices.md` for detailed examples

**Label positioning problems**:
- Position labels in clear space (above/below/beside lines)
- Never place labels in the middle where they overlap content
- Use smaller font sizes (12px) for better proportion

**Detailed guidance**: See `references/drawio-layout-best-practices.md`

### 3. HTML Entity Escaping

**CRITICAL**: Confluence requires proper HTML entity escaping to prevent "Error parsing xhtml" errors.

**Use**: `scripts/html_escape.py` for all page content before submission

**Rules**:
- Escape `&` → `&amp;` (except in existing entities)
- Escape `<` → `&lt;` in text context (NOT in HTML tags)
- Escape `>` → `&gt;` in text context (NOT in HTML tags)

**Common unescaped patterns**:
- "score < 4", "value > 0" → requires escaping
- "Hook & Payoff", "Setup & Teardown" → requires escaping

**Reference**: `references/storage_format.md` for complete escaping rules

### 4. Updating Existing Pages

**Update workflow**:
```bash
# 1. Fetch current page HTML
python3 scripts/wiki_get_page.py --page-id 3647578884 --format html > current.html

# 2. Use Edit tool to modify specific sections (NEVER Write tool!)
# Preserve all <ac:*> tags

# 3. Update page (automatic validation prevents markup loss)
python3 scripts/wiki_create_page.py --update 3647578884 --version N --file current.html
```

**Key rules**:
- Use **Edit tool** for updates (Write tool loses inline comments and markup)
- Validation is **automatic** - script fails if markup would be lost
- Preserve `<ac:inline-comment-marker>` tags (active discussions)

### 5. Index Page Curation

**MANDATORY**: After creating or updating any page, update the relevant index page.

**Key index pages**:
- Engineering Proposals (ID: `3137163046`) - default for technical documentation
- Development Standards + Resources (ID: `3162741123`) - coding standards
- Core Service Architecture (ID: `3498290022`) - service architecture
- Engineering Inventory (ID: `3178898959`) - service catalogs
- Service Inventory (ID: `3518591586`) - detailed service docs

**Process**:
1. Identify appropriate index page for new content
2. Get current index page content
3. Add link to new page in appropriate section
4. Update with incremented version number

**Reference**: `references/wiki_structure.md` for index page IDs and curation protocol

### 6. Jira Integration

**Preferred method**: Use Jira's LINK facility (remote links API)

```bash
curl -X POST -H "Authorization: Bearer $JIRA_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "object": {
      "url": "WIKI_URL",
      "title": "Wiki Page Title"
    }
  }' \
  "https://jira.corp.adobe.com/rest/api/2/issue/ISSUE-KEY/remotelink"
```

**Fallback**: Add comment with wiki link (use Wiki syntax, NOT Markdown)

**Reference**: `references/wiki_structure.md` for linking examples

## Workflow Decision Tree

Use this decision tree to determine the appropriate workflow:

```
User request
    │
    ├─ Read EXISTING wiki page from URL?
    │   │
    │   ├─ Use scripts/wiki_get_page.py --url "URL"
    │   └─ Parse and display content
    │
    ├─ Create NEW wiki page?
    │   │
    │   ├─ Search first with /search-work
    │   ├─ Read source documentation (READMEs, code)
    │   ├─ Verify you have technical design/requirements
    │   ├─ Choose parent page (default: Engineering Proposals)
    │   ├─ Generate diagrams (draw.io + PlantUML)
    │   ├─ Create page content (use template from assets/)
    │   ├─ Escape HTML entities (scripts/html_escape.py)
    │   ├─ Create page via REST API
    │   ├─ Update index page (MANDATORY)
    │   ├─ Link to Jira ticket
    │   └─ Provide wiki URL to user
    │
    ├─ Update EXISTING wiki page?
    │   │
    │   ├─ Fetch current page HTML (scripts/wiki_get_page.py --format html)
    │   ├─ Use EDIT TOOL (NOT Write) to surgically modify specific sections
    │   ├─ Preserve all <ac:inline-comment-marker> and other markup
    │   ├─ Escape HTML entities (scripts/html_escape.py)
    │   ├─ Update page with incremented version (validation automatic)
    │   ├─ If validation fails, script stops with error - fix and retry
    │   └─ Cross-link related pages if needed
    │
    ├─ Create DIAGRAM only?
    │   │
    │   ├─ Draw.io (architecture)?
    │   │   ├─ Use assets/drawio_template.xml as starting point
    │   │   ├─ Create diagram with orthogonal edge routing
    │   │   ├─ **MANDATORY**: Validate with render_drawio.py
    │   │   │  ├─ Render to PNG
    │   │   │  └─ Visually inspect for layout issues
    │   │   ├─ Fix any lines cutting through boxes (add waypoints)
    │   │   ├─ Re-validate until clean
    │   │   └─ Upload to wiki using wiki_attach_file.py
    │   │
    │   └─ PlantUML (sequence)?
    │       ├─ Generate PlantUML syntax
    │       ├─ Validate with scripts/render_plantuml.py
    │       ├─ Inspect preview PNG for visual issues
    │       ├─ Fix any syntax/rendering errors
    │       └─ Provide plantuml macro syntax
    │
    └─ Search/find existing documentation?
        └─ Use /search-work slash command
```

## Authentication

**Environment variable**: `WIKI_TOKEN` contains personal access token

**Authentication header** (REQUIRED for all API calls):
```bash
Authorization: Bearer $WIKI_TOKEN
```

**Token management**: If expired, get new token at https://wiki.corp.adobe.com/plugins/personalaccesstokens/usertokens.action

**VPN required**: Adobe VPN connection required for all wiki operations

**Reference**: `references/confluence_api.md` for authentication patterns

## Page Structure Best Practices

Use this structure for technical documentation (see `assets/page_template.html`):

1. **Title + Status Info**: Page title, status, author, date
2. **Table of Contents**: Auto-generated from headers
3. **Overview**: High-level summary (2-3 paragraphs)
4. **Problem Statement**: What problem this solves
5. **Architecture**: Visual diagrams + explanations
   - Architecture diagram (draw.io)
   - Sequence diagram (PlantUML)
6. **Implementation Details**: Key patterns (code examples ≤5 lines)
7. **Testing**: Test strategy and locations
8. **Key Files**: Table of important file paths
9. **Related Links**: Jira tickets, wiki pages, external docs

**Writing style**:
- Present tense (document current state, not historical changes)
- Concise and technical (for engineer audience)
- Specific (exact file paths, function names)
- Scannable (headers, tables, lists)

**Reference**: `references/storage_format.md` for Confluence macros and HTML elements

## Common Operations

### Create Wiki Page
```bash
# 1. Prepare content (escape HTML entities)
python3 scripts/html_escape.py /tmp/content.html /tmp/escaped.html

# 2. Create page
curl -X POST -H "Authorization: Bearer $WIKI_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "type": "page",
    "title": "Page Title",
    "ancestors": [{"id": "3137163046"}],
    "space": {"key": "GenStudio"},
    "body": {
      "storage": {
        "value": "ESCAPED_HTML_CONTENT",
        "representation": "storage"
      }
    }
  }' \
  "https://wiki.corp.adobe.com/rest/api/content"
```

### Upload Draw.io Diagram as Attachment
```bash
# Upload .drawio file as attachment
python3 scripts/wiki_attach_file.py --page-id 3650098139 --file diagram.drawio --comment "Architecture diagram"

# List attachments on a page
python3 scripts/wiki_attach_file.py --page-id 3650098139 --list

# Embed in page using drawio macro
<ac:structured-macro ac:name="drawio" ac:schema-version="1">
  <ac:parameter ac:name="diagramName">diagram.drawio</ac:parameter>
  <ac:parameter ac:name="simpleViewer">false</ac:parameter>
  <ac:parameter ac:name="zoom">1</ac:parameter>
</ac:structured-macro>
```

### Validate PlantUML
```bash
# Check for syntax errors before submission
python3 scripts/validate_plantuml.py /tmp/sequence.plantuml
```

## Error Handling

**"Error parsing xhtml"**: Content has unescaped HTML entities
- Solution: Use `scripts/html_escape.py`

**"403 Forbidden" / "anonymous" user**: Authentication failed
- Check VPN connected
- Verify `$WIKI_TOKEN` is set
- Ensure Bearer keyword in header

**"Version conflict"**: Page modified since last read
- Get latest version and retry

**PlantUML syntax errors**: Invalid diagram syntax
- Use `scripts/validate_plantuml.py` to catch errors
- Check for multi-line arrow labels
- Verify blocks are closed with `end`

**Reference**: `references/confluence_api.md` for complete error handling guide

## Critical Reminders

1. **Use Edit tool for updates** (NEVER Write) - automatic validation prevents markup loss
2. **Search before creating**: Use `/search-work` to avoid duplicates
3. **Update index pages**: MANDATORY after creating/updating pages
4. **Escape HTML entities**: Use `scripts/html_escape.py` before submission
5. **Never fabricate details**: Request missing requirements, don't invent
6. **VPN required**: All operations need Adobe VPN connection

## Resources

### scripts/
- `wiki_get_page.py` - Fetch wiki page content from URL or page ID
- `wiki_create_page.py` - Create or update wiki pages with **automatic markup validation**
- `wiki_attach_file.py` - Upload attachments (draw.io diagrams, files) to wiki pages
- `html_escape.py` - Safe HTML entity escaping for Confluence storage format
- `render_plantuml.py` - PlantUML syntax validation and PNG preview generation
- `render_drawio.py` - Draw.io XML validation and image preview generation
- `validate_plantuml.py` - Legacy PlantUML syntax validation (use render_plantuml.py instead)

### references/
- `confluence_api.md` - REST API endpoints, authentication, error handling
- `diagram_styles.md` - Draw.io shapes, PlantUML patterns, color schemes
- `plantuml-best-practices.md` - PlantUML syntax best practices, common errors, troubleshooting
- `storage_format.md` - Confluence storage format, macros, HTML elements
- `wiki_structure.md` - GenStudio page hierarchy, index pages, curation protocol

### assets/
- `drawio_template.xml` - Basic architecture diagram template
- `plantuml_sequence_template.txt` - Sequence diagram starter template
- `page_template.html` - Complete Confluence page structure template

## Examples

### Example 1: Create Architectural Documentation

**User request**: "Document the new parallel evaluation architecture with diagrams"

**Workflow**:
1. Search first: `/search-work` for related "evaluation" documentation
2. Read source: Check codebase READMEs, architectural documents
3. Verify inputs: Confirm you have architect's technical design
4. Create draw.io architecture diagram using `assets/drawio_template.xml`
5. Create PlantUML sequence diagram using `assets/plantuml_sequence_template.txt`
6. Build page content using `assets/page_template.html`
7. Escape HTML: `python3 scripts/html_escape.py content.html escaped.html`
8. Create page under Engineering Proposals (ID: `3137163046`)
9. Upload draw.io diagram (no extension)
10. Update Engineering Proposals index page
11. Link to Jira ticket using remote links API
12. Provide wiki URL to user

### Example 2: Create PlantUML Sequence Diagram

**User request**: "Create a sequence diagram showing the agent execution flow"

**Workflow**:
1. Generate PlantUML based on `assets/plantuml_sequence_template.txt`
2. Include parallel blocks for concurrent operations
3. Add activation/deactivation for lifecycle
4. Validate: `python3 scripts/validate_plantuml.py diagram.plantuml`
5. Fix any syntax errors (multi-line labels, unclosed blocks)
6. Provide plantuml macro syntax for embedding

### Example 3: Update Existing Wiki Page

**User request**: "Update the Marketing Agent wiki page with new metrics"

**Workflow**:
1. Fetch current page: `python3 scripts/wiki_get_page.py --page-id PAGE_ID --format html > current.html`
2. Use Edit tool to surgically modify specific sections (add new metrics)
   - **CRITICAL**: Preserve all `<ac:inline-comment-marker>` tags
   - Only modify the content that needs changing
3. Escape HTML: `python3 scripts/html_escape.py current.html escaped.html`
4. Update page: `python3 scripts/wiki_create_page.py --update PAGE_ID --version N --file escaped.html`
   - Script automatically validates markup preservation
   - If validation fails, script exits with error showing what would be lost
   - Fix issues and retry
5. Check if related pages need cross-linking
6. Confirm success with user

## Common Mistakes

**❌ Using Write tool for updates** → Use Edit tool (Write loses all markup)
**❌ Working from summary instead of HTML** → Always fetch with `--format html`
**❌ "Draft updated version" = create from scratch** → Always Edit existing HTML file

## When NOT to Use This Skill

- When user asks about GitHub (use gh CLI, not wiki)
- When documentation belongs in codebase (README.md files)
- When creating internal team notes (use Slack or private docs)
- When user needs to edit wiki in browser (provide URL and instructions)
