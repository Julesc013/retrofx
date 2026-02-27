# RetroFX Palettes

## Structured Palette Families (Fast)

Structured palettes are arithmetic mappings in shader code and avoid expensive nearest-color scans:

- `mono2`, `mono4`, `mono8`, `mono16`
- `vga16` (bounded loop of 16 entries)
- `cube32` (3x3x3 + grayscale blend)
- `cube64` (4x4x4 cube)
- `cube128` (4x4x8 deterministic cube)
- `cube256` (6x6x6 + grayscale ramp blend)

Complexity:

- `mono*` and `cube*`: `O(1)`
- `vga16`: `O(16)`

No `O(256)` per-pixel nearest loop is used for these modes.

## Custom Palette Files

Custom palettes are supported for up to 32 colors:

```toml
[palette]
kind = "custom"
size = 16
custom_file = "palettes/c64.txt"
```

File format:

- one color per line: `#RRGGBB`
- comment lines begin with `# ` (hash + space)
- blank lines are ignored

Example: `palettes/c64.txt`

Custom palette quantization uses bounded nearest-color search:

- complexity `O(N)`, `N <= 32`

## Performance Notes

- Structured palettes are preferred for maximum throughput.
- Custom palettes remain practical because the search bound is fixed at 32.
- RetroFX intentionally avoids temporal buffers and multi-pass palette processing.
