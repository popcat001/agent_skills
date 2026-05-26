# PlantUML Best Practices for Confluence

## Critical: Multi-Line Note Syntax

**PROBLEM**: Using inline `\n` escape sequences in note blocks causes "cannot create group" errors in Confluence.

### ❌ WRONG - Inline Escape Sequences
```plantuml
note right of Sensor: Event filters:\n- X-Github-Event: pull_request\n- action: opened
end note
```

**Error**: "cannot create group" when rendered in Confluence

### ✅ CORRECT - Multi-Line Block
```plantuml
note right of Sensor
Event filters:
- X-Github-Event: pull_request
- action: opened
end note
```

**Result**: Renders correctly with proper line breaks

## Validation Before Upload

**MANDATORY**: Always validate PlantUML diagrams before uploading to Confluence.

```bash
python3 ~/.claude/skills/confluence-wiki/scripts/render_plantuml.py \
  --input diagram.plantuml \
  --output-dir /tmp/previews/

# Inspect the generated PNG
open /tmp/previews/diagram.png
```

## Common Issues and Fixes

### 1. "Cannot Create Group" Errors
**Cause**: Inline escape sequences in notes, groups, or boxes
**Fix**: Use multi-line blocks with actual line breaks

### 2. Text Not Wrapping in Notes
**Cause**: Long single-line text
**Fix**: Break into multiple lines manually

### 3. Special Characters in Labels
**Cause**: Unescaped special characters
**Fix**: Escape or use quotes around labels

## Confluence PlantUML Specifics

- Confluence uses standard PlantUML engine but with **strict parsing**
- Errors that work in some renderers (draw.io, VS Code extensions) **will fail in Confluence**
- Always test with official PlantUML CLI (`brew install plantuml`)
- Use `plantuml -checksyntax` before uploading

## Best Practices

1. **Always use multi-line blocks** for notes, never inline `\n`
2. **Validate locally** with `render_plantuml.py` before upload
3. **Keep it simple** - complex nesting can cause issues
4. **Use consistent indentation** for readability
5. **Test in Confluence** before marking documentation as complete

## Quick Reference

**Note blocks**:
```plantuml
note left of Actor
Line 1
Line 2
Line 3
end note
```

**Note over multiple actors**:
```plantuml
note over Actor1, Actor2
Multi-line content
without \n escapes
end note
```

**Groups** (use sparingly):
```plantuml
group Description
  Actor -> Service: request
  Service --> Actor: response
end
```

## Sequence Diagram Best Practices

### Actor/Participant Naming
- Use clear, descriptive names
- Avoid special characters in participant names
- Use `participant` keyword for better control over display names

```plantuml
participant "GitHub Webhook" as GH
participant "Event Sensor" as Sensor
participant "Agent Hub" as Hub
```

### Message Flow
- Keep messages concise
- Use notes for detailed information, not message labels
- Use `activate` and `deactivate` to show processing

```plantuml
GH -> Sensor: POST /webhook
activate Sensor
note right of Sensor
Validates payload
Filters events
end note
Sensor -> Hub: route(event)
deactivate Sensor
```

### Multi-Line Messages
- Use `\n` for multi-line messages (but NOT in notes!)
- Alternatively, use notes below messages

```plantuml
# Option 1: Multi-line message
Actor -> Service: Process request\nwith parameters

# Option 2: Message + note (preferred for clarity)
Actor -> Service: Process request
note right
Request parameters:
- param1: value1
- param2: value2
end note
```

## Component Diagram Best Practices

### Component Organization
- Group related components in packages
- Use clear interface definitions
- Avoid overly complex nesting

```plantuml
package "GitHub Integration" {
  component [Event Sensor]
  component [Webhook Handler]
}

package "Agent System" {
  component [Agent Hub]
  component [Agent Orchestrator]
}

[Webhook Handler] --> [Event Sensor]
[Event Sensor] --> [Agent Hub]
```

### Interface Definition
```plantuml
interface "Webhook API" as WebhookAPI
interface "Event Bus" as EventBus

[Event Sensor] -- WebhookAPI
[Event Sensor] --> EventBus
[Agent Hub] --> EventBus
```

## Deployment Diagram Best Practices

### Node Representation
```plantuml
node "Production Environment" {
  component [API Server]
  database "PostgreSQL" as DB
}

cloud "External Services" {
  component [GitHub]
  component [Slack]
}

[API Server] --> DB
[API Server] ..> [GitHub]: webhook
[API Server] ..> [Slack]: notifications
```

## Styling and Formatting

### Use Skinparam for Consistency
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam componentStyle rectangle
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 12

' Your diagram here

@enduml
```

### Color Usage
```plantuml
skinparam component {
  BackgroundColor<<critical>> LightCoral
  BackgroundColor<<external>> LightBlue
  BackgroundColor<<internal>> LightGreen
}

component [API] <<critical>>
component [GitHub] <<external>>
component [Database] <<internal>>
```

## Testing Workflow

### 1. Local Syntax Validation
```bash
plantuml -checksyntax diagram.plantuml
```

### 2. Visual Preview
```bash
python3 ~/.claude/skills/confluence-wiki/scripts/render_plantuml.py \
  --input diagram.plantuml \
  --output-dir /tmp/preview
```

### 3. Test in Confluence
- Upload to draft page first
- Verify rendering
- Check all interactive elements work
- Confirm mobile/tablet rendering

## Troubleshooting

### Diagram Won't Render
1. Check syntax: `plantuml -checksyntax file.plantuml`
2. Look for inline `\n` in notes
3. Check for unmatched `end` statements
4. Verify all participants are defined

### Formatting Issues
1. Remove inline escape sequences
2. Use multi-line blocks
3. Check for special characters
4. Validate indentation

### "Cannot Create Group" Error
**Most common cause**: Inline `\n` in note blocks

**Solution**: Convert to multi-line format:
```plantuml
# Change this:
note right: Line 1\nLine 2

# To this:
note right
Line 1
Line 2
end note
```

## Advanced Patterns

### Conditional Logic Display
```plantuml
alt Success Case
  Service -> Database: save(data)
  Database --> Service: success
else Failure Case
  Service -> Logger: log(error)
  Logger --> Service: logged
end
```

### Loop Representation
```plantuml
loop for each item
  Service -> Processor: process(item)
  Processor --> Service: result
end
```

### Parallel Processing
```plantuml
par Processing Branch 1
  Service -> API1: request
  API1 --> Service: response
and Processing Branch 2
  Service -> API2: request
  API2 --> Service: response
end
```

## Resources

- Official PlantUML Documentation: https://plantuml.com/
- Sequence Diagram Guide: https://plantuml.com/sequence-diagram
- Component Diagram Guide: https://plantuml.com/component-diagram
- Confluence PlantUML Macro: https://confluence.atlassian.com/doc/plantuml-macro-1018115293.html

## Quick Checklist Before Upload

- [ ] Syntax validated with `plantuml -checksyntax`
- [ ] Visual preview generated and reviewed
- [ ] No inline `\n` in note blocks
- [ ] All multi-line content uses proper blocks
- [ ] Special characters properly escaped
- [ ] Diagram is readable at standard zoom levels
- [ ] Tested in draft Confluence page
- [ ] Mobile/responsive rendering verified
