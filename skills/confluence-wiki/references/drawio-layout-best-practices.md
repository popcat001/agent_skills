# Draw.io Layout Best Practices

## Overview

This document captures best practices for creating professional, publication-ready draw.io diagrams, particularly for technical architecture documentation. These practices emerged from fixing layout issues in Kubernetes network isolation diagrams.

## Core Principle: Lines Should Never Cut Through Boxes

The most common and unprofessional layout mistake is allowing connection lines (arrows, dashed lines, etc.) to pass directly through boxes, containers, or other visual elements. This makes diagrams look sloppy and hard to read.

**Solution**: Use waypoints to route lines AROUND boxes, not through them.

## Waypoint Routing Technique

### Basic Waypoint Syntax

Draw.io uses `<mxPoint>` elements within the edge geometry to define waypoints:

```xml
<mxCell id="edge1" edge="1" parent="1" source="box1" target="box2">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="200"/>  <!-- First waypoint -->
      <mxPoint x="300" y="400"/>  <!-- Second waypoint -->
      <mxPoint x="500" y="400"/>  <!-- Third waypoint -->
    </Array>
  </mxGeometry>
</mxCell>
```

### When to Use Waypoints

Add waypoints whenever:
- A direct line between source and target would cross through a box
- A line needs to route around namespace containers
- Multiple lines need to avoid overlapping with each other
- Labels need to be positioned away from other content

### Orthogonal (Right-Angle) Routing

For technical diagrams, use orthogonal routing with the `edgeStyle=orthogonalEdgeStyle` attribute:

```xml
<mxCell id="edge1" style="endArrow=classic;html=1;strokeColor=#82b366;strokeWidth=3;
             edgeStyle=orthogonalEdgeStyle"
         edge="1" parent="1" source="box1" target="box2">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="450" y="485" />
      <mxPoint x="450" y="360" />
      <mxPoint x="300" y="360" />
      <mxPoint x="300" y="495" />
    </Array>
  </mxGeometry>
</mxCell>
```

This creates clean, professional right-angle turns that are standard in technical architecture diagrams.

## Practical Examples from This Project

### Example 1: Routing Blocked Connection Around Namespaces

**Problem**: A red dashed "blocked" line needed to show that ephemeral PR environments cannot access Stage VPC resources. The direct line cut through multiple namespace boxes.

**Solution**: Route the line UP and AROUND the namespaces:

```xml
<mxCell id="arrow-no-vpc-1"
       style="endArrow=none;html=1;strokeColor=#b85450;strokeWidth=2;dashed=1;
              endFill=0;startArrow=none;startFill=0;
              edgeStyle=orthogonalEdgeStyle"
       edge="1" parent="1" source="ext-stage" target="eph1-ns">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="90" y="290" />   <!-- Start from source -->
      <mxPoint x="90" y="90" />    <!-- Go UP above all boxes -->
      <mxPoint x="580" y="90" />   <!-- Go RIGHT above boxes -->
      <mxPoint x="580" y="178" />  <!-- Come DOWN to target -->
    </Array>
  </mxGeometry>
</mxCell>
```

**Key insight**: Going UP and OVER provides the cleanest routing when horizontal paths are blocked.

### Example 2: Isolation Lines Between Namespaces

**Problem**: Lines showing network isolation between namespaces cut horizontally through Service boxes.

**Solution**: Route lines UP above the namespaces, then back down:

```xml
<mxCell id="arrow-eph1-stage"
       style="endArrow=none;html=1;strokeColor=#b85450;strokeWidth=2;dashed=1;
              endFill=0;edgeStyle=orthogonalEdgeStyle"
       edge="1" parent="1" source="eph1-pods" target="stage-pods">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="450" y="485" />  <!-- Exit from source pod -->
      <mxPoint x="450" y="360" />  <!-- Go UP above namespace -->
      <mxPoint x="300" y="360" />  <!-- Go LEFT above namespace -->
      <mxPoint x="300" y="495" />  <!-- Come DOWN to target -->
    </Array>
  </mxGeometry>
</mxCell>
```

**Key insight**: For horizontal isolation lines, route vertically around obstacles using a rectangular path.

## Label Positioning Best Practices

### Position Labels Outside Content Areas

Instead of placing labels in the middle of lines where they overlap with other content:

**❌ Bad**: Label positioned where line crosses boxes
```xml
<mxCell id="block-x-ns" value="✗ Isolated"
       style="text;html=1;align=center;verticalAlign=middle;fontSize=14;
              fontStyle=1;fontColor=#b85450"
       vertex="1" parent="1">
  <mxGeometry x="415" y="465" width="65" height="40" as="geometry" />
</mxCell>
```

**✅ Good**: Label positioned above boxes in clear space
```xml
<mxCell id="block-x-ns" value="✗ Isolated"
       style="text;html=1;align=center;verticalAlign=middle;fontSize=12;
              fontStyle=1;fontColor=#b85450"
       vertex="1" parent="1">
  <mxGeometry x="325" y="340" width="90" height="30" as="geometry" />
</mxCell>
```

### Label Sizing

- Keep labels concise: "✗ Isolated" is better than "✗\nIsolated" (multi-line)
- Use appropriate font sizes: 11-14px for labels, 20px+ for titles
- Give labels enough width to avoid text wrapping

## Spacing and Alignment Guidelines

### Minimum Spacing Between Elements

- **Between boxes**: 20px minimum padding
- **Between namespaces**: 30-40px for clarity
- **Around labels**: 10px minimum clearance

### Grid Alignment

- Use grid="1" and gridSize="10" in mxGraphModel
- Snap all elements to 10px grid increments
- Align boxes horizontally and vertically for professional appearance

Example:
```xml
<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1">
```

### Container Padding

When placing elements inside container boxes (like namespaces):
- Leave 15-20px padding from top for title
- Leave 20px padding on left/right sides
- Leave 15px padding on bottom

Example:
```xml
<mxCell id="stage-ns" value="genstudio--agent-hub-stage (Stage Environment)"
       style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;
              strokeColor=#82b366;verticalAlign=top;align=left;
              spacingLeft=15;spacingTop=15;fontSize=14;fontStyle=1"
       vertex="1" parent="1">
  <mxGeometry x="100" y="120" width="460" height="280" as="geometry" />
</mxCell>
```

## Visual Validation Workflow

### Essential Workflow: Edit → Render → Inspect → Iterate

Never trust the diagram XML alone. Always render to PNG and visually inspect:

```bash
# 1. Edit the diagram XML file
vim sources/my-diagram.drawio

# 2. Render to PNG using Docker
cd /path/to/workspace
docker run --rm -v "$(pwd):/data" rlespinasse/drawio-export \
  --format png --output /data/renders sources/my-diagram.drawio

# 3. Visually inspect the rendered PNG
open renders/my-diagram-PageName.png

# 4. If issues remain, repeat from step 1
```

### What to Check During Visual Inspection

**Critical checks**:
- ✓ No lines cutting through boxes
- ✓ All labels fully visible and positioned clearly
- ✓ Adequate spacing between all elements
- ✓ Consistent alignment (boxes on same horizontal level)
- ✓ No overlapping text

**Quality checks**:
- ✓ Professional orthogonal routing (right angles, not diagonal)
- ✓ Consistent stroke widths (2-3px for main arrows)
- ✓ Color consistency (same meaning = same color)
- ✓ Font size hierarchy (titles > labels > body text)

## Common Pitfalls to Avoid

### 1. Direct Line Routing

**❌ Never do this**:
```xml
<mxCell id="bad-edge" edge="1" parent="1" source="box1" target="box2">
  <mxGeometry relative="1" as="geometry" />  <!-- No waypoints! -->
</mxCell>
```

When boxes are in the way, this will create a line straight through them.

**✅ Always add waypoints when needed**:
```xml
<mxCell id="good-edge" edge="1" parent="1" source="box1" target="box2">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="200"/>
      <mxPoint x="500" y="200"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 2. Insufficient Waypoints

Using too few waypoints results in lines that still clip corners or edges of boxes.

**Rule of thumb**: For routing around a rectangular obstacle, use 4 waypoints minimum (one for each corner of the path around the box).

### 3. Labels in the Middle of Crossing Lines

Labels positioned where lines cross other content become unreadable.

**Solution**: Always position labels in clear space, preferably:
- Above or below the line (not in the middle)
- In empty space between major elements
- Outside container boundaries

### 4. Inconsistent Edge Styles

Mixing different edge routing styles in the same diagram looks unprofessional.

**Best practice**: Choose one style (orthogonal recommended) and use it consistently:
```xml
edgeStyle=orthogonalEdgeStyle
```

### 5. Skipping Visual Validation

The biggest mistake is editing XML without rendering to PNG.

**Why this fails**:
- Waypoint coordinates might be slightly off
- Labels might overlap in ways not obvious in XML
- Line thickness might look different when rendered
- Colors might not be as distinct as expected

**Always render and visually inspect before uploading to wiki**.

## Color Coding Best Practices

### Establish Clear Color Meanings

Use consistent colors throughout diagrams:

**Our standard**:
- **Green (#82b366)**: Stage environment, allowed traffic
- **Purple (#9673a6)**: Ephemeral environments
- **Red (#b85450)**: Blocked traffic, isolation
- **Blue (#0e8088)**: External resources (Internet, VPC)
- **Orange (#d79b00)**: Ingress, peering connections
- **Yellow (#fff2cc)**: Policies, quotas, RBAC

### Stroke vs Fill Colors

- Use **stroke color** for borders and arrows
- Use **lighter fill color** of the same hue for box backgrounds
- Example: Green boxes use fillColor=#d5e8d4, strokeColor=#82b366

## Testing Before Wiki Upload

### Pre-Upload Checklist

Before uploading diagrams to Confluence wiki:

**Technical validation**:
- [ ] Diagram renders successfully with Docker
- [ ] No error messages during rendering
- [ ] PNG file size reasonable (< 500KB for typical diagrams)
- [ ] All pages in multi-page diagrams render

**Visual validation**:
- [ ] No lines cut through boxes
- [ ] All text fully visible and readable
- [ ] Labels positioned clearly
- [ ] Adequate spacing (minimum 20px between elements)
- [ ] Elements aligned on grid
- [ ] Consistent arrow routing style
- [ ] Color coding consistent with legend

**Content validation**:
- [ ] All elements properly labeled
- [ ] Legend included and complete
- [ ] Title clearly visible
- [ ] Technical accuracy verified

## Advanced Techniques

### Routing Multiple Parallel Lines

When multiple lines need to follow similar paths around obstacles:

1. Calculate a primary path with waypoints
2. Offset subsequent lines by 20-30px horizontally or vertically
3. Use the same number of waypoints for consistency

Example:
```xml
<!-- First line -->
<Array as="points">
  <mxPoint x="300" y="200"/>
  <mxPoint x="300" y="400"/>
</Array>

<!-- Second parallel line (offset by 30px) -->
<Array as="points">
  <mxPoint x="330" y="200"/>
  <mxPoint x="330" y="400"/>
</Array>
```

### Creating "Avoiding" Zones

For complex diagrams, plan "traffic lanes":
- Reserve certain horizontal bands for connections
- Reserve vertical columns for crossing lines
- Route all similar connections through the same lane

This creates organized, predictable routing patterns.

## Tool Configuration

### Recommended mxGraphModel Settings

```xml
<mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1"
              tooltips="1" connect="1" arrows="1" fold="1" page="1"
              pageScale="1" pageWidth="1400" pageHeight="900">
```

**Key settings**:
- `grid="1"`: Enable grid snapping
- `gridSize="10"`: 10px grid increments
- `guides="1"`: Show alignment guides
- `pageWidth/pageHeight`: Set canvas size appropriately

### Docker Rendering Command

Standard command for rendering:
```bash
docker run --rm -v "$(pwd):/data" rlespinasse/drawio-export \
  --format png \
  --output /data/renders \
  sources/diagram-name.drawio
```

**Options**:
- `--format png`: Export as PNG (also supports pdf, svg)
- `--output /data/renders`: Output directory
- Last argument: Source .drawio file

## Summary: The Golden Rules

1. **Never let lines cut through boxes** - Use waypoints to route around obstacles
2. **Use orthogonal routing** - Right-angle turns look more professional
3. **Position labels in clear space** - Away from boxes and crossing lines
4. **Maintain consistent spacing** - Minimum 20px between elements
5. **Align elements on grid** - Use 10px grid snapping
6. **Always visually validate** - Render to PNG and inspect before uploading
7. **Iterate until perfect** - Edit → Render → Inspect → Repeat
8. **Use consistent colors** - Establish meaning for each color
9. **Test before upload** - Complete the pre-upload checklist
10. **Document waypoint coordinates** - Makes future edits easier

## Future Improvements

These practices should be integrated into:
- Confluence-wiki skill diagram generation
- Automated validation scripts
- Draw.io templates with pre-defined styles
- CI/CD pipeline checks for diagram quality

By following these practices, all future draw.io diagrams will have professional, publication-ready layouts on the first upload, avoiding the need for post-upload fixes.
