# Architecture

The project is intentionally static so it can run from a local file, a simple HTTP server, or GitHub Pages.

## Runtime flow

1. `index.html` defines the operator console regions.
2. `src/styles.css` handles the responsive dashboard layout and status states.
3. `src/app.js` owns simulator state, safety policy evaluation, command limiting, event logging, and canvas rendering.

## Interface regions

- Operator View: safety map, geofence, robot pose, nearby human marker, obstacles, and desired command vector.
- Command Controls: speed limit, arm/disarm, deadman hold, commanded output, and emergency stop.
- Safety Interlocks: policy checks for link health, human proximity, platform attitude, battery, motor thermal state, and geofence.
- Telemetry: live simulated robot state and event log.

## Data model

The app keeps a single state object in `src/app.js`. Scenario targets are blended into the live telemetry every second to create a realistic signal without external services.

The command gate is derived from:

- Emergency stop state.
- Failed interlocks.
- Arm state.
- Deadman state.
- Active warnings and risk score.
- Operator speed limit.

This keeps command output deterministic and easy to inspect.
