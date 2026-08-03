# Quick Start

## Running the MCP Server

### Stdio Mode (Claude Desktop, Cursor)

```bash
tuvi-mcp
```

### Streamable HTTP Mode

```bash
tuvi-mcp --http
```

Override host and port:
```bash
tuvi-mcp --http --host 127.0.0.1 --port 1850
```

## Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tuvi-horoscope": {
      "command": "/path/to/venv/bin/tuvi-mcp",
      "args": []
    }
  }
}
```

## Cursor Integration

Settings → Features → MCP → "+ Add New MCP Server":

- **Name:** TuViMCP
- **Type:** command
- **Command:** `/path/to/venv/bin/tuvi-mcp`

## Python Library Usage

```python
from tuvi_mcp import Horoscope, BirthInfo, Gender, Calendar

h = Horoscope.from_birth(
    name="Nguyễn Văn A",
    year=1995, month=6, day=10,
    hour="14:30",          # also "Ngọ", 14, or 7 (branch index)
    gender="Nam",          # also "male", 1, True, or Gender.MALE
    calendar="solar",
)

# Birth chart
chart = h.chart()
print(chart.thien_ban["can_nam"], chart.thien_ban["chi_nam"])
print(len(chart.dia_ban), "cungs")

# Transit (Vận Hạn)
van_han = h.transit(year=2026, month=5, day=15)
print(van_han["target_period"]["current_year_can_chi"])

# Auspicious day
auspicious = h.auspicious(day=27, month=7, year=2026)

# Render chart as PNG (uses bundled Roboto Unicode font by default)
path = h.render_chart(chart, year=2026)

# Optionally specify custom TTF font files
path = h.render_chart(chart, year=2026, font_path="/path/to/custom_font.ttf")

# JSON-serializable output
json_data = chart.to_dict()

# SQLite database
from tuvi_mcp.database import init_db, save_horoscope, list_saved_horoscopes
init_db()
save_horoscope("My Chart", chart.to_dict())
profiles = list_saved_horoscopes()
```

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `pip install tuvi-mcp-server` fails on Pillow | Platform missing build tools | `pip install --only-binary=:all: tuvi-mcp-server` |
| `ModuleNotFoundError: ephem` | Optional dep not installed | Ignore; only needed for advanced calendar features |
| `tuvi-mcp: command not found` | venv not active | Use full path: `.venv/bin/tuvi-mcp` or `python -m tuvi_mcp` |
| `PEP 668: externally-managed-environment` | System Python with package manager rules | Use a virtual environment (`python3 -m venv .venv`) |
| `pytest: command not found` | Test deps not installed | `pip install -e ".[test]"` |

## Running Tests

```bash
pytest
```
