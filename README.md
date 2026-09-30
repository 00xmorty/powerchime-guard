# PowerChime Guard

PowerChime Guard is a tiny, read-only macOS CLI that explains the current charging-chime preference and power-source snapshot. It can print narrowly scoped, reversible `defaults` commands, but never runs them.

## Run

Requires macOS and Python 3. No packages, administrator access, or install step are required.

```sh
curl -LO https://github.com/00xmorty/powerchime-guard/releases/latest/download/powerchime-guard
chmod +x powerchime-guard
./powerchime-guard
./powerchime-guard --plan-disable
```

To print the command that removes the override and returns control to macOS defaults:

```sh
./powerchime-guard --plan-restore
```

Plans are text only. Review and run a printed command manually if you choose. JSON output and a deterministic offline path are available:

```sh
./powerchime-guard --json
./powerchime-guard --input tests/fixture.json --plan-disable
```

In v0.2.0, compare two manually saved offline JSON snapshots without contacting a service:

```sh
./powerchime-guard --input before.json --compare after.json --json
```

Each file uses the four keys shown in `tests/fixture.json`. Only recognized `AC Power` / `Battery Power` values are classified; unfamiliar power-source text remains `unknown`. A transition is a clue, not evidence of the cause of a chime. Review local snapshots for sensitive text before sharing. Comparison does not collect or save snapshots for you.

Exit codes: `0` inspection completed; `2` unsupported platform, invalid fixture, failed query, or timeout.

## Example

Synthetic output, not a real Mac report:

```text
PowerChime Guard — read-only charging-chime inspector
Preference: default
Power source: AC Power
PowerChime app: present
- No user override is stored; macOS controls the default behavior.
- AC power is connected now; this snapshot cannot detect earlier reconnects.
- Repeated chimes can indicate power negotiation or a loose cable; muting is not a repair.
LIMIT: one snapshot cannot prove why a chime repeated or certify a cable/dock.
```

## Safety

- Strictly read-only: live mode calls only `defaults read`, `pmset -g ps`, and a fixed system-app existence check.
- Disable/restore plans are printed as text; PowerChime Guard never executes `defaults write` or `defaults delete`.
- No `sudo`, process kill, file deletion, LaunchAgent, daemon, telemetry, upload, or network access.
- Output can reveal whether AC power is connected. Review it before sharing.
- The restore plan deletes only `ChimeOnAllHardware`, not the preference domain.

## Limitations

- Live inspection supports macOS only; Linux is supported only for tests and fixtures.
- `ChimeOnAllHardware` is an undocumented, version-sensitive preference and may stop working in future macOS releases.
- A stored preference does not prove whether a sound played, whether the setting took effect immediately, or whether it survives an OS update.
- One power-source snapshot cannot detect intermittent reconnects, measure cable quality, certify a charger/dock, or diagnose hardware.
- Two offline snapshots cannot establish when a chime occurred or prove a particular dock/cable caused a transition; unknown states are not treated as disconnections.
- Silencing a repeated chime can hide a power-negotiation symptom. Inspect the cable, port, charger, and dock instead of treating mute as a repair.
- Manual commands change user preferences. Record the prior state and understand the command before running one.

## Development

```sh
python3 -m py_compile powerchime-guard
python3 -m unittest discover -s tests -v
./powerchime-guard --input tests/fixture.json --plan-disable
```

## License

MIT. See [LICENSE](LICENSE).
