# GenStudio Wiki Structure

## Root Pages

**GenStudio: Engineering** (ID: `3137154789`)
- URL: https://wiki.corp.adobe.com/display/GenStudio/GenStudio%3A+Engineering
- Top-level landing page for all GenStudio engineering documentation
- **⚠️ DO NOT create pages directly under root** - requires special permissions

## Key Index Pages (MUST be curated)

When creating or updating wiki pages, you MUST update relevant index pages to maintain discoverability.

### 1. Engineering Proposals (ID: `3137163046`)
- URL: https://wiki.corp.adobe.com/display/GenStudio/Engineering+Proposals
- **Purpose**: Architectural documentation, technical designs, feature proposals
- **Use for**: Architecture diagrams, design documents, technical RFCs
- **Default parent**: Use this as default parent for new technical documentation
- **Curation**: Add newly created proposals to this index

### 2. Development Standards + Resources (ID: `3162741123`)
- **Purpose**: Coding standards, testing standards, development guides
- **Use for**: Best practices, coding conventions, development workflows
- **Curation**: Add new standards or guidelines documentation here

### 3. Core Service Architecture (ID: `3498290022`)
- **Purpose**: System architecture, service designs, infrastructure
- **Use for**: Service architecture diagrams, infrastructure documentation
- **Curation**: Add new service architecture documentation here

### 4. Engineering Inventory (ID: `3178898959`)
- **Purpose**: Service catalogs, component inventories, technical inventories
- **Use for**: Listings of services, libraries, tools, components
- **Curation**: Add new services or components to inventory

### 5. Service Inventory (ID: `3518591586`)
- **Purpose**: Detailed service documentation, API docs, service guides
- **Use for**: Individual service documentation, operational guides
- **Curation**: Add detailed service documentation here

## Page Creation Protocol

### Step 1: Choose Parent Page

**Default**: Engineering Proposals (ID: `3137163046`)

**Decision tree**:
- Architecture/design documentation → Engineering Proposals
- Coding standards/best practices → Development Standards + Resources
- Service architecture → Core Service Architecture
- Service catalog entry → Engineering Inventory
- Detailed service docs → Service Inventory

### Step 2: Create Page

Use Confluence REST API with proper parent page ID:

```json
{
  "type": "page",
  "title": "Your Page Title",
  "ancestors": [{"id": "PARENT_PAGE_ID"}],
  "space": {"key": "GenStudio"},
  "body": {
    "storage": {
      "value": "<content>",
      "representation": "storage"
    }
  }
}
```

### Step 3: Update Index (MANDATORY)

After creating page, update the appropriate index page:

1. Get current index page content
2. Add link to new page in appropriate section
3. Use consistent formatting with existing entries
4. Update with incremented version number

## Index Curation Format

**Standard link format**:
```html
<p><a href="/pages/viewpage.action?pageId=PAGE_ID">Page Title</a> - Brief description (Created: YYYY-MM-DD)</p>
```

**Categorized format** (if index has sections):
```html
<h3>Category Name</h3>
<ul>
  <li><a href="/pages/viewpage.action?pageId=PAGE_ID">Page Title</a> - Brief description</li>
</ul>
```

## Distributed Curation Philosophy

Every wiki interaction is an opportunity to improve wiki health:

1. **Create**: New page → Update index (MANDATORY)
2. **Update**: Existing page → Check if related pages need linking (BEST EFFORT)
3. **View Index**: Browse → Note obvious stale content (OPPORTUNISTIC)
4. **Cross-link**: Add links between related documentation (BEST EFFORT)

## Linking to Jira

**Preferred Method**: Use Jira's LINK facility (remote links API)

```bash
curl -X POST \
  -H "Authorization: Bearer $JIRA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "object": {
      "url": "WIKI_URL",
      "title": "Wiki Page Title"
    }
  }' \
  "https://jira.corp.adobe.com/rest/api/2/issue/ISSUE-KEY/remotelink"
```

**Fallback Method**: Add comment with wiki link (use Wiki syntax, NOT Markdown)

```bash
curl -X POST \
  -H "Authorization: Bearer $JIRA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "h2. 📖 Technical Documentation\n\n[Page Title|WIKI_URL]\n\n*Includes*:\n* Item 1\n* Item 2"
  }' \
  "https://jira.corp.adobe.com/rest/api/2/issue/ISSUE-KEY/comment"
```

## Search Integration

Before creating new documentation, search for existing content using `/search-work`:
- Avoids duplication
- Finds related pages for cross-linking
- Discovers stale content that could be updated instead

## Stale Content Detection

When viewing index pages, flag obviously outdated content:

```html
<p>⚠️ <strong>Content may be outdated</strong> - Last updated: YYYY-MM-DD. Review before using.</p>
```

Consider pages >90 days old without updates potentially stale.
