# Repository Guidelines

## Project Structure & Module Organization
This repo is a Tauri-first desktop assistant workspace.
- `apps/desktop-ui/`: desktop UI and Rust host (`src-tauri`).
- `.github/workflows/`: CI workflows for Rust/Tauri validation.
- Root docs (`README.md`, `ROADMAP.md`) define direction and delivery plan.

## Build, Test, and Development Commands
- `cd apps/desktop-ui/src-tauri && cargo tauri dev`: run desktop app in Tauri dev mode.
- `cd apps/desktop-ui/src-tauri && cargo tauri build`: build desktop bundle.
- `cargo check --manifest-path apps/desktop-ui/src-tauri/Cargo.toml`: validate Rust host.

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
There is currently no dedicated unit/integration test framework configured. CI validates Rust host checks on PRs.
- Minimum local check: `cargo check --manifest-path apps/desktop-ui/src-tauri/Cargo.toml` before commit or PR.
- For UI changes, perform manual validation in `cargo tauri dev` and confirm build succeeds.

## Commit & Pull Request Guidelines
Git history currently mixes patch-version commits (for example `0.0.91`) with short, informal messages. For collaboration, prefer clear imperative commit subjects like `Fix hero animation timing`.
- Keep commits focused and scoped to one change.
- In PRs, include: purpose, key files changed, validation steps run, and screenshots/GIFs for UI updates.
- Link related issues/tasks when applicable.

## Security & Deployment Tips
- Do not commit secrets or environment tokens.

## Planning & Product Context
- Read `ROADMAP.md` before starting any task.
- Every task must align with the roadmap plan; if scope changes, update `ROADMAP.md` in the same work session to reflect status, sequencing, or new tasks.
- Before implementing, mark the selected roadmap task as `in progress` in `ROADMAP.md` to claim a lock and avoid overlap with other agents.
- When implementation is complete, mark that roadmap task as `Done` in `ROADMAP.md` (and include completion date when possible) before handing off.
- Maintain a `specs/` folder with feature-level product documentation (one file per feature/workstream when possible).
- Keep `specs/` and `ROADMAP.md` synchronized: roadmap items should reference corresponding specs, and specs should reference roadmap phase/task IDs.
- Treat `ROADMAP.md` and `specs/` as required context so agents always know current product direction and the next priority.
