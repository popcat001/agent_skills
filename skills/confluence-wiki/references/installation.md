# Diagram Validation Tools Installation

This guide covers installation of tools for local diagram validation and rendering.

## PlantUML

### Installation via Homebrew

```bash
brew install plantuml
```

### Verification

```bash
plantuml -version
```

Expected output:
```
PlantUML version 1.2025.9 (Mon Sep 08 10:56:38 CDT 2025)
(GPL source distribution)
...
Installation seems OK. File generation OK
```

### Requirements

- **Java Runtime**: PlantUML requires Java (installed automatically by Homebrew)
- **Graphviz**: Required for advanced diagram types (installed as dependency)

### Usage

The `render_plantuml.py` script uses PlantUML via command line:
- Syntax validation: `plantuml -checksyntax <file>`
- PNG rendering: `plantuml -tpng -o <output_dir> <file>`

### Testing PlantUML Installation

Verify PlantUML is working correctly:

```bash
# Check version
plantuml -version

# Test syntax checking
echo '@startuml
Alice -> Bob: test
@enduml' > /tmp/test.plantuml

plantuml -checksyntax /tmp/test.plantuml
```

Expected output: "No syntax error" or specific line numbers if errors exist.

**Test with multi-line notes** (common issue):

```bash
cat > /tmp/test-notes.plantuml <<'EOF'
@startuml
participant Service

note right of Service
Line 1
Line 2
Line 3
end note

Service -> Database: query
@enduml
EOF

plantuml -checksyntax /tmp/test-notes.plantuml
```

Expected output: "No syntax error"

**Test rendering**:

```bash
plantuml -tpng -o /tmp /tmp/test-notes.plantuml
open /tmp/test-notes.png
```

Expected: PNG image with proper multi-line note rendering.

## Draw.io Validation with Docker (REQUIRED)

Docker is **mandatory** for draw.io diagram validation before wiki upload.

```bash
# Verify Docker is running
docker ps

# Pull draw.io export image
docker pull rlespinasse/drawio-export:latest

# Test rendering
docker run --rm -v "$(pwd):/data" rlespinasse/drawio-export \
  --format png --output /data/test.drawio
```

**Why Docker is required**:
- Only way to visually validate diagrams before wiki upload
- Catches layout issues that are invisible in XML
- Prevents publishing sloppy diagrams with lines through boxes

### Docker Installation

**Requirements**: Docker Desktop installed and running

```bash
# Pull the image
docker pull rlespinasse/drawio-export

# Verify Docker is running
docker info
```

**Common Docker issues**:
- **"Cannot connect to Docker daemon"**: Start Docker Desktop application
- **Image pull timeout**: Check internet connection and Docker Hub access
- **Permission denied**: On Linux, add user to `docker` group

**Usage notes**:
- Docker option automatically used if `drawio-exporter` not found
- Requires absolute paths for file mounts
- Performance is sufficient for validation workflow

### Alternative: Cargo Installation (Optional)

**Requirements**: Rust toolchain with edition 2024 support

```bash
cargo install drawio-exporter
```

**Current limitation**: The latest version (1.4.0) requires Rust edition 2024, which is not yet stable in the default Rust toolchain (as of Cargo 1.83.0).

**Recommendation**: Use Docker option for consistent, reliable validation

**Verification**:
```bash
which drawio-exporter
drawio-exporter --version
```

## Tool Selection Logic

The `render_drawio.py` script automatically detects available tools:

1. **First check**: Look for `drawio-exporter` in PATH
2. **Fallback**: Check for Docker and verify daemon is running
3. **Error**: If neither available, provide installation instructions

## Verification Test

Test both scripts after installation:

### Test PlantUML

```bash
# Create test diagram
cat > /tmp/test.plantuml <<'EOF'
@startuml
actor User
participant Service
User -> Service: Request
Service --> User: Response
@enduml
EOF

# Validate and render
python3 ~/.claude/skills/confluence-wiki/scripts/render_plantuml.py \
  --input /tmp/test.plantuml \
  --output-dir /tmp/test-output/

# Check output
open /tmp/test-output/test.png
```

### Test Draw.io

```bash
# Use provided template
python3 ~/.claude/skills/confluence-wiki/scripts/render_drawio.py \
  --input ~/.claude/skills/confluence-wiki/assets/drawio_template.xml \
  --output-dir /tmp/test-output/ \
  --format png

# Check output
open /tmp/test-output/drawio_template.png
```

## Troubleshooting

### PlantUML Issues

**"plantuml: command not found"**
- Install via Homebrew: `brew install plantuml`
- Verify installation: `which plantuml`

**"Java not found"**
- PlantUML requires Java runtime
- Reinstall PlantUML: `brew reinstall plantuml` (installs Java as dependency)

**"Graphviz not found"**
- Required for certain diagram types
- Reinstall PlantUML: `brew reinstall plantuml` (installs Graphviz as dependency)

**Rendering timeout**
- Complex diagrams may exceed 60-second timeout
- Simplify diagram or increase timeout in script

### Draw.io Issues

**"No rendering tool available"**
- Neither Cargo nor Docker installation found
- Choose one installation method and verify with commands above

**Cargo installation fails (edition2024 error)**
- Expected with current stable Rust (1.83.0)
- Use Docker option instead
- Wait for Rust edition 2024 stabilization

**Docker "Cannot connect to daemon"**
- Start Docker Desktop application
- Verify with: `docker info`
- Check Docker Desktop is running in system tray/menu bar

**Docker image pull fails**
- Check internet connection
- Verify Docker Hub access (no corporate proxy blocking)
- Try manual pull: `docker pull rlespinasse/drawio-export`

**Permission denied (Linux)**
- Add user to docker group: `sudo usermod -aG docker $USER`
- Log out and back in for group changes to take effect

### General Issues

**Script import errors**
- Verify Python 3 is installed: `python3 --version`
- Check script permissions: `chmod +x scripts/*.py`

**Output directory not created**
- Scripts create output directories automatically
- Check filesystem permissions for parent directory
- Use absolute paths to avoid working directory issues

## Alternative Tools

### PlantUML Alternatives

- **PlantUML Server**: Web-based rendering (no local installation)
  - URL: http://www.plantuml.com/plantuml/
  - Not recommended for validation (requires internet, slower)

- **PlantUML JAR**: Direct Java execution
  - Download from https://plantuml.com/download
  - Requires manual Java classpath management

### Draw.io Alternatives

- **Draw.io Desktop**: GUI application
  - Not suitable for automation
  - Manual export required

- **Headless Chrome**: Browser-based rendering
  - Complex setup, not recommended
  - Requires Puppeteer or similar

## Maintenance

### Updating Tools

**PlantUML**:
```bash
brew upgrade plantuml
```

**Cargo drawio-exporter** (when available):
```bash
cargo install --force drawio-exporter
```

**Docker image**:
```bash
docker pull rlespinasse/drawio-export
```

### Checking for Updates

**PlantUML version**:
```bash
plantuml -version
# Check https://plantuml.com/download for latest
```

**Docker image**:
```bash
docker images | grep drawio-export
# Check Docker Hub for latest tag
```

## Future Improvements

Potential enhancements to consider:

1. **Alternative draw.io renderers**: Explore Python-based XML-to-image conversion
2. **Caching**: Cache rendered images to avoid re-rendering unchanged diagrams
3. **Parallel rendering**: Render multiple diagrams concurrently
4. **SVG support**: Add SVG output for scalable diagrams
5. **Diff visualization**: Show visual diff when updating existing diagrams
