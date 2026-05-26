# Draw.io Quick Reference

## Waypoint Routing Pattern (4 points)
```xml
<Array as="points">
  <mxPoint x="exitX" y="clearY"/>    <!-- 1. Exit perpendicular -->
  <mxPoint x="routeX" y="clearY"/>   <!-- 2. Move past obstacle -->
  <mxPoint x="routeX" y="enterY"/>   <!-- 3. Turn toward target -->
  <mxPoint x="enterX" y="enterY"/>   <!-- 4. Enter target -->
</Array>
```

## Pre-Upload Checklist
- [ ] Docker render completed
- [ ] PNG visually inspected
- [ ] No lines through boxes
- [ ] Labels positioned cleanly
- [ ] Professional appearance

Full guide: See drawio-layout-best-practices.md
