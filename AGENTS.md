# Repository Guidelines

## Project Structure & Module Organization
This repo is a webpack-based frontend portfolio site.
- `src/`: application source.
- `src/index.jsx`: app entry point.
- `src/styles/`: SCSS modules (feature-focused files like `hero_header.scss`, `projects.scss`).
- `src/data/`: JSON content (for example `work.json`, `blog_articles.json`).
- `src/assets/`: static assets (icons, images, 3D model files).
- `scripts/`: helper shell scripts (`minify.sh`, resume upload/update scripts).
- `dist/`: generated build output (do not hand-edit).

## Build, Test, and Development Commands
- `npm start`: run webpack dev server in development mode.
- `npm run start:prod`: run webpack dev server using production mode.
- `npm run build`: clean `dist/` and create production bundle via `webpack.prod.js`.
- `npm run build:dev`: build with the development webpack config.
- `./verify.sh`: project verification script; runs both dev and prod builds.
- `npm run bundle-report`: build with stats and open bundle analyzer on port `4200`.

## Coding Style & Naming Conventions
- Indentation is 4 spaces (`.editorconfig`, `.prettierrc`).
- Use single quotes and semicolons (`.prettierrc`).
- ESLint extends `eslint:recommended` and `react-app`; run linting before opening PRs.
- Keep component/module filenames in lowercase with underscores where already established (for example `contact_form.jsx`, `growth_chart.jsx`).
- Keep styles split by feature in `src/styles/` instead of one monolithic stylesheet.
- For UI consistency, reuse existing control styles from shared/global rules (`src/styles/style.scss`) and avoid introducing one-off button borders/shapes unless a section explicitly requires a new visual pattern.
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
There is currently no dedicated unit/integration test framework configured. CI (`.github/workflows/webpack.yml`) validates builds on PRs using Node 18 and `npm run build`.
- Minimum local check: `./verify.sh` before commit or PR.
- For UI changes, perform manual validation in `npm start` and confirm production build succeeds.

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
- Maintain a `specs/` folder with feature-level product documentation (one file per feature/workstream when possible).
- Keep `specs/` and `ROADMAP.md` synchronized: roadmap items should reference corresponding specs, and specs should reference roadmap phase/task IDs.
- Treat `ROADMAP.md` and `specs/` as required context so agents always know current product direction and the next priority.
