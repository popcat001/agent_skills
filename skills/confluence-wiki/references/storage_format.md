# Confluence Storage Format Reference

## Overview

Confluence uses XHTML-based storage format with custom `ac:` (Atlassian Confluence) macros for special features like diagrams and code blocks.

## HTML Elements

### Headers
```html
<h1>Top Level Header</h1>
<h2>Section Header</h2>
<h3>Subsection Header</h3>
<h4>Minor Header</h4>
```

### Text Formatting
```html
<p>Paragraph text</p>
<strong>Bold text</strong>
<em>Italic text</em>
<u>Underlined text</u>
<code>inline code</code>
```

### Lists
```html
<ul>
  <li>Unordered item 1</li>
  <li>Unordered item 2</li>
</ul>

<ol>
  <li>Ordered item 1</li>
  <li>Ordered item 2</li>
</ol>
```

### Tables
```html
<table class="wrapped">
  <thead>
    <tr>
      <th>Header 1</th>
      <th>Header 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cell 1</td>
      <td>Cell 2</td>
    </tr>
  </tbody>
</table>
```

### Links
```html
<a href="https://example.com">External link</a>
<a href="/pages/viewpage.action?pageId=12345">Internal wiki link</a>
```

### Horizontal Rule
```html
<hr />
```

## Confluence Macros

### Macro Structure
```xml
<ac:structured-macro ac:name="macro-name" ac:schema-version="1">
  <ac:parameter ac:name="parameter-name">parameter-value</ac:parameter>
  <ac:plain-text-body><![CDATA[
    Content goes here
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

### Code Block Macro
```xml
<ac:structured-macro ac:name="code" ac:schema-version="1">
  <ac:parameter ac:name="language">typescript</ac:parameter>
  <ac:parameter ac:name="linenumbers">true</ac:parameter>
  <ac:parameter ac:name="theme">Midnight</ac:parameter>
  <ac:plain-text-body><![CDATA[
// Your code here
const example = "Hello, World!";
console.log(example);
  ]]></ac:plain-text-body>
</ac:structured-macro>
```

**Supported languages**: typescript, javascript, python, java, bash, json, xml, sql, yaml, go, rust, etc.

### Info/Warning/Note Panels
```xml
<ac:structured-macro ac:name="info" ac:schema-version="1">
  <ac:rich-text-body>
    <p>Information message here</p>
  </ac:rich-text-body>
</ac:structured-macro>

<ac:structured-macro ac:name="warning" ac:schema-version="1">
  <ac:rich-text-body>
    <p>Warning message here</p>
  </ac:rich-text-body>
</ac:structured-macro>

<ac:structured-macro ac:name="note" ac:schema-version="1">
  <ac:rich-text-body>
    <p>Note message here</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Table of Contents
```xml
<ac:structured-macro ac:name="toc" ac:schema-version="1">
  <ac:parameter ac:name="maxLevel">3</ac:parameter>
  <ac:parameter ac:name="minLevel">1</ac:parameter>
</ac:structured-macro>
```

### PlantUML Diagram
```xml
<ac:structured-macro ac:name="plantuml" ac:schema-version="1">
  <ac:parameter ac:name="atlassian-macro-output-type">INLINE</ac:parameter>
  <ac:plain-text-body><![CDATA[@startuml
title My Diagram
participant A
participant B
A -> B: message
@enduml]]></ac:plain-text-body>
</ac:structured-macro>
```

### Draw.io Diagram (Embedded)
```xml
<ac:structured-macro ac:name="inc-drawio" ac:schema-version="1">
  <ac:parameter ac:name="diagramName">Architecture-Diagram</ac:parameter>
  <ac:parameter ac:name="includedDiagram">1</ac:parameter>
  <ac:parameter ac:name="width">800</ac:parameter>
  <ac:parameter ac:name="pageId">PAGE_ID</ac:parameter>
  <ac:parameter ac:name="" />
</ac:structured-macro>
```

**Note**: draw.io diagram must be uploaded as attachment first (without file extension).

### Expand/Collapse Section
```xml
<ac:structured-macro ac:name="expand" ac:schema-version="1">
  <ac:parameter ac:name="title">Click to expand</ac:parameter>
  <ac:rich-text-body>
    <p>Hidden content that appears when expanded</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Quote Block
```xml
<ac:structured-macro ac:name="quote" ac:schema-version="1">
  <ac:rich-text-body>
    <p>Quoted text here</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

## HTML Entity Escaping

**CRITICAL**: All special characters in text content must be properly escaped.

### Required Escaping Rules

1. **Ampersands**: `&` → `&amp;` (except when already part of entity)
2. **Less-than in text**: `<` → `&lt;` (NOT in HTML tags)
3. **Greater-than in text**: `>` → `&gt;` (NOT in HTML tags)

### Common Unescaped Patterns to Fix

- `score < 4` → `score &lt; 4`
- `value > 0` → `value &gt; 0`
- `Hook & Payoff` → `Hook &amp; Payoff`
- `Setup & Teardown` → `Setup &amp; Teardown`

### Use html_escape.py Script

```bash
# Escape HTML entities safely
python3 scripts/html_escape.py input.html output.html

# Or pipe mode
cat input.html | python3 scripts/html_escape.py > output.html
```

The script handles:
- Safe ampersand escaping (doesn't double-escape)
- Context-aware `<` and `>` escaping (preserves HTML tags)
- Validation warnings for potentially unescaped content

## Common Errors

### "Error parsing xhtml"

**Cause**: Unescaped special characters in content

**Solution**: Use `html_escape.py` script before submission

**Example error indicators**:
- "Unexpected character ' ' (code 32)"
- "Error parsing xhtml"
- Content renders blank on wiki

### "Invalid storage format"

**Cause**: Malformed XML in macros or HTML

**Solution**:
- Check XML escaping in macro content
- Use `<![CDATA[...]]>` for code/diagram content
- Validate closing tags match opening tags

### "Macro not found"

**Cause**: Incorrect macro name or unsupported macro

**Solution**: Verify macro name spelling:
- `inc-drawio` (NOT `drawio` or `draw-io`)
- `plantuml` (NOT `plant-uml`)
- `code` (NOT `codeblock`)

## Best Practices

1. **Use CDATA for literal content**: Wrap code, diagrams, and literal text in `<![CDATA[...]]>`
2. **Escape HTML entities**: Always escape `&`, `<`, `>` in prose using script
3. **Validate before submission**: Check escaping and macro syntax
4. **Keep HTML semantic**: Use proper heading hierarchy, semantic elements
5. **Limit inline styles**: Use Confluence's built-in styling
6. **Test with small payloads**: For large content, test structure with subset first
