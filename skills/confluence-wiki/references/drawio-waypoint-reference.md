# Waypoint Coordinate Reference

Quick reference for all waypoint fixes applied to diagrams.

## Environment Topology Diagram

### Red X "No VPC Access" Line
**Edge ID**: `arrow-no-vpc-1`
**Purpose**: Show blocked VPC peering from Stage VPC Resources to PR-1 namespace
**Strategy**: Route UP and AROUND namespaces

```xml
<mxCell id="arrow-no-vpc-1"
       style="endArrow=none;html=1;strokeColor=#b85450;strokeWidth=2;dashed=1;
              endFill=0;startArrow=none;startFill=0;
              exitX=1;exitY=0.3;exitDx=0;exitDy=0;
              entryX=0;entryY=0.25;entryDx=0;entryDy=0;
              edgeStyle=orthogonalEdgeStyle"
       edge="1" parent="1" source="ext-stage" target="eph1-ns">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="90" y="290" />   <!-- Exit Stage VPC Resources -->
      <mxPoint x="90" y="90" />    <!-- Go UP above cluster -->
      <mxPoint x="580" y="90" />   <!-- Go RIGHT above namespaces -->
      <mxPoint x="580" y="178" />  <!-- Come DOWN to PR-1 edge -->
    </Array>
  </mxGeometry>
</mxCell>
```

**Associated Label**: Red X symbol
```xml
<mxCell id="block-x-1" value="✗"
       style="text;html=1;align=center;verticalAlign=middle;fontSize=24;
              fontStyle=1;fontColor=#b85450"
       vertex="1" parent="1">
  <mxGeometry x="560" y="70" width="40" height="40" as="geometry" />
</mxCell>
```

**Key Points**:
- Line routes above cluster boundary at y=90
- Red X positioned in clear space above namespaces
- 4 waypoints create clean rectangular path

---

## Network Isolation Diagram

### Isolation Line: Stage ↔ PR-1
**Edge ID**: `arrow-eph1-stage`
**Purpose**: Show network isolation between Stage and Ephemeral PR-1 namespaces
**Strategy**: Route UP and AROUND namespace containers

```xml
<mxCell id="arrow-eph1-stage"
       style="endArrow=none;html=1;strokeColor=#b85450;strokeWidth=2;dashed=1;
              endFill=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;
              entryX=1;entryY=0.5;entryDx=0;entryDy=0;
              edgeStyle=orthogonalEdgeStyle"
       edge="1" parent="1" source="eph1-pods" target="stage-pods">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="450" y="485" />  <!-- Exit PR-1 pods westward -->
      <mxPoint x="450" y="360" />  <!-- Go UP above namespaces -->
      <mxPoint x="300" y="360" />  <!-- Go LEFT toward Stage -->
      <mxPoint x="300" y="495" />  <!-- Come DOWN to Stage pods -->
    </Array>
  </mxGeometry>
</mxCell>
```

**Associated Label**: "✗ Isolated"
```xml
<mxCell id="block-x-ns" value="✗ Isolated"
       style="text;html=1;align=center;verticalAlign=middle;fontSize=12;
              fontStyle=1;fontColor=#b85450"
       vertex="1" parent="1">
  <mxGeometry x="325" y="340" width="90" height="30" as="geometry" />
</mxCell>
```

**Key Points**:
- Line routes above namespaces at y=360
- Label positioned in clear space above routing
- Avoids cutting through Stage Service and PR-1 Service boxes

---

### Isolation Line: PR-1 ↔ PR-2
**Edge ID**: `arrow-eph1-eph2`
**Purpose**: Show network isolation between Ephemeral PR-1 and PR-2 namespaces
**Strategy**: Route UP and AROUND namespace containers

```xml
<mxCell id="arrow-eph1-eph2"
       style="endArrow=none;html=1;strokeColor=#b85450;strokeWidth=2;dashed=1;
              endFill=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;
              entryX=0;entryY=0.5;entryDx=0;entryDy=0;
              edgeStyle=orthogonalEdgeStyle"
       edge="1" parent="1" source="eph1-svc" target="eph2-svc">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="840" y="485" />   <!-- Exit PR-1 Service eastward -->
      <mxPoint x="840" y="360" />   <!-- Go UP above namespaces -->
      <mxPoint x="1015" y="360" />  <!-- Go RIGHT toward PR-2 -->
      <mxPoint x="1015" y="485" />  <!-- Come DOWN to PR-2 Service -->
    </Array>
  </mxGeometry>
</mxCell>
```

**Associated Label**: "✗ Isolated"
```xml
<mxCell id="block-x-eph" value="✗ Isolated"
       style="text;html=1;align=center;verticalAlign=middle;fontSize=12;
              fontStyle=1;fontColor=#b85450"
       vertex="1" parent="1">
  <mxGeometry x="865" y="340" width="90" height="30" as="geometry" />
</mxCell>
```

**Key Points**:
- Line routes above namespaces at y=360 (same as PR-1↔Stage line)
- Label positioned in clear space above routing
- Changed connection to use Service boxes (eph1-svc, eph2-svc) instead of Pods for better visual balance
- Avoids cutting through PR-1 Service and PR-2 Service boxes

---

## Waypoint Routing Patterns

### Pattern 1: Horizontal Blocking → Vertical Routing

When direct horizontal path is blocked:
1. Exit source vertically (up or down)
2. Move horizontally parallel to desired direction
3. Enter target vertically

**Example**: Both isolation lines in Network Isolation diagram use this pattern

### Pattern 2: Multiple Obstacles → High-Level Routing

When multiple obstacles block the path:
1. Go UP above all obstacles
2. Move horizontally at this high level
3. Come DOWN to target

**Example**: Red X line in Environment Topology diagram routes above entire cluster

### Pattern 3: Rectangular Obstacle Avoidance

Standard 4-waypoint pattern for going around a rectangle:
1. Waypoint 1: Move perpendicular to avoid obstacle
2. Waypoint 2: Move parallel past obstacle
3. Waypoint 3: Turn toward target
4. Waypoint 4: Align with target

**Used in**: All three fixed lines

---

## Coordinate Calculation Tips

### Finding Y-coordinate for "Above Namespaces" Routing

1. Find the lowest Y-coordinate of namespace top edges
2. Subtract 30-40px for clearance
3. Use this as the routing level

**Example**:
- Stage namespace top: y=380
- PR namespaces top: y=380
- Routing level: y=360 (20px clearance)

### Finding X-coordinate for Vertical Routing Segments

1. Find the center or edge of source/target boxes
2. Add/subtract 20-30px for clearance from box edges
3. Use consistent X-coordinates for parallel segments

**Example**:
- PR-1 Service right edge: x=795
- Vertical routing segment: x=840 (45px clearance)

### Label Positioning Relative to Waypoints

Position labels near waypoint intersections but with offset:
- If routing at y=360, position label at y=340 (20px above)
- Center label horizontally between relevant boxes
- Give label width of 90-120px

---

## Visual Validation Checklist

After adding waypoints, render and check:
- [ ] Line does not pass through any boxes
- [ ] Line does not clip corners of boxes
- [ ] Label is fully visible in clear space
- [ ] Line uses orthogonal (right-angle) routing
- [ ] Waypoints create smooth rectangular path
- [ ] Color and stroke width are consistent

---

## Common Mistakes to Avoid

### Mistake 1: Insufficient Clearance
```xml
<!-- BAD: Only 10px clearance -->
<mxPoint x="370" y="370" />  <!-- Too close to namespace at y=380 -->

<!-- GOOD: 20-30px clearance -->
<mxPoint x="360" y="360" />  <!-- Safe distance from y=380 -->
```

### Mistake 2: Missing Waypoint
```xml
<!-- BAD: Only 3 waypoints for rectangular path -->
<Array as="points">
  <mxPoint x="450" y="485" />
  <mxPoint x="450" y="360" />
  <mxPoint x="300" y="495" />  <!-- MISSING horizontal waypoint! -->
</Array>

<!-- GOOD: 4 waypoints for complete rectangle -->
<Array as="points">
  <mxPoint x="450" y="485" />
  <mxPoint x="450" y="360" />
  <mxPoint x="300" y="360" />  <!-- Essential horizontal segment -->
  <mxPoint x="300" y="495" />
</Array>
```

### Mistake 3: Diagonal Routing
```xml
<!-- BAD: Missing orthogonalEdgeStyle -->
style="endArrow=none;html=1;strokeColor=#b85450;strokeWidth=2;dashed=1"

<!-- GOOD: Includes orthogonal routing -->
style="endArrow=none;html=1;strokeColor=#b85450;strokeWidth=2;dashed=1;
       edgeStyle=orthogonalEdgeStyle"
```

---

## Integration Notes

These waypoint patterns should be:
1. Integrated into confluence-wiki skill diagram generation
2. Used as templates for similar routing scenarios
3. Referenced when fixing future diagram layout issues
4. Incorporated into automated diagram validation scripts

The coordinates are specific to these diagrams but the patterns are universal.
