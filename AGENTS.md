# Repository Guidelines

## Project Structure & Module Organization
This repo contains two implementations:

### Rust Standalone MVP
- `deskling-character/`: Rust/egui standalone character application
- Build: `cd deskling-character && cargo build --release`
- Run: `cargo run --release`

### Full Product (Tauri + Python)
- `apps/desktop-ui/`: Tauri desktop UI (Vite frontend + Rust host).
- `apps/ipc-hub/`: Python IPC hub service.
- `services/`: Python services (`agent-core`, `automation-service`, `voice-service`, `skin-service`).
- `shared/schemas/`: shared JSON message/tool schemas.
- `configs/`: local config templates and permission policies.
- `scripts/`: helper shell scripts.

## Build, Test, and Development Commands

### Rust Standalone MVP
- `cd deskling-character && cargo build --release`: build optimized binary
- `cargo run --release`: run character demo
- `./verify.sh`: verify implementation

### Full Product (Tauri + Python)
- `npm run dev`: run `apps/desktop-ui` frontend dev server.
- `npm run tauri:dev`: run desktop app in Tauri dev mode.
- `npm run build`: build frontend assets for desktop packaging.
- `npm run tauri:build`: build desktop bundle via Tauri.
- `./verify.sh`: project verification script (`npm run build` + Rust `cargo check`).
- `./scripts/dev-up.sh`: start local dev stack (`ipc-hub`, `agent-core`, `desktop-ui`).
- `python3 scripts/typed_chat_smoke.py`: run typed-chat IPC smoke test.

## Coding Style & Naming Conventions
- Indentation is 4 spaces (`.editorconfig`, `.prettierrc`).
- Use single quotes and semicolons (`.prettierrc`).
- Keep JS/TS modules in lowercase with underscores where already established.
- Keep styles split by feature in `apps/desktop-ui/src/` instead of one monolithic stylesheet.
- Prefer shared UI tokens/styles over one-off control treatments.
- For theme toggles, show the icon for the target mode (`moon` in light mode, `sun` in dark mode) and keep nav icon buttons visually neutral (no custom circular border treatment unless explicitly requested).
- Do not add arrow glyphs (`→`, `←`) in action labels and do not style action text as bold/oversized by default; keep action labels neutral unless explicitly requested.

## Agent Response Style
- Start every user-facing response with `hi` plus one short motivating line.
- Work style: telegraph style preferred; noun-phrases are fine; drop nonessential grammar; minimize token usage.

## Frontend Aesthetics
- Avoid generic “AI slop” UI; outputs should be opinionated and visually distinctive.
- Commit to a clear palette per page/feature, define it with CSS variables, and prefer bold accents over timid gradients.
- Use motion sparingly: 1-2 high-impact moments (for example staged reveal/stagger), not many random micro-animations.
- Add depth in backgrounds (gradients, texture, or subtle patterns) instead of flat defaults.
- Avoid purple-on-white cliches, generic component grids, and predictable layouts.

## Testing Guidelines
There is currently no dedicated unit/integration test framework configured. CI validates frontend build and Rust host check on PRs.
- Minimum local check: `./verify.sh` before commit or PR.
- For UI changes, perform manual validation in `npm run tauri:dev` and confirm build succeeds.

## Commit & Pull Request Guidelines
Git history currently mixes patch-version commits (for example `0.0.91`) with short, informal messages. For collaboration, prefer clear imperative commit subjects like `Fix hero animation timing`.
- Keep commits focused and scoped to one change.
- In PRs, include: purpose, key files changed, validation steps run, and screenshots/GIFs for UI updates.
- Link related issues/tasks when applicable.

## Security & Deployment Tips
- Do not commit secrets; deployment uses AWS CLI credentials from your environment (`deploy.sh`).
- `deploy.sh` targets bucket `hson.fr` and can invalidate CloudFront when a parameter is passed; run only after a successful `npm run build`.

## Planning & Product Context
- Read `ROADMAP.md` before starting any task.
- Every task must align with the roadmap plan; if scope changes, update `ROADMAP.md` in the same work session to reflect status, sequencing, or new tasks.
- Before implementing, mark the selected roadmap task as `in progress` in `ROADMAP.md` to claim a lock and avoid overlap with other agents.
- When implementation is complete, mark that roadmap task as `Done` in `ROADMAP.md` (and include completion date when possible) before handing off.
- Maintain a `specs/` folder with feature-level product documentation (one file per feature/workstream when possible).
- Keep `specs/` and `ROADMAP.md` synchronized: roadmap items should reference corresponding specs, and specs should reference roadmap phase/task IDs.
- Treat `ROADMAP.md` and `specs/` as required context so agents always know current product direction and the next priority.
