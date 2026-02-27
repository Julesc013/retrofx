# RetroFX Testing

Run all commands from repo root.

## Baseline Checks

```bash
shellcheck scripts/retrofx || true
./scripts/retrofx list
./scripts/retrofx doctor
./scripts/retrofx preview
```

## Apply / Off

```bash
./scripts/retrofx apply passthrough
./scripts/retrofx off
```

Expected behavior:

- `active/` is regenerated atomically.
- previous `active/` snapshot appears in `state/backups/`.
- `state/last_good/` is updated after successful apply.

## Strict Parser Checks

Create a temporary invalid profile and confirm parse failure:

- unknown key -> must fail
- missing required key -> must fail
- out-of-range value -> must fail

## Validation/Fallback Checks

- If `picom` is unavailable, apply should warn and continue safely.
- If shader/config validation fails, active config should remain usable.
- If `active/` is empty and `last_good/` exists, fallback restore should succeed.

## Backend Scope Checks

Set scope flags in profile and verify hooks:

- `scope.x11 = true` triggers `backends/x11-picom/apply.sh`.
- `scope.tty = true` triggers scaffold notice.
- `scope.tuigreet = true` triggers scaffold notice.
