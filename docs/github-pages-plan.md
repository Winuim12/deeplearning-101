# GitHub Pages migration

User approved a static browser app and requested ready-to-push source plus deployment commands. Do not push or publish to an unspecified repository. Preserve the existing visual design, original slides, bank and academic review status.

## Decisions

- Default application: React/Vite static site, no API service required.
- Reuse pure grading/selection functions in `server/domain.mjs`; retain legacy Node server as an optional reference, not a runtime dependency.
- Export bank, module/source metadata and original PDFs during build. Public page images already live under public/assets.
- Native IndexedDB keeps progress and exam history per browser, scoped to site path. Atomic read/write transactions prevent two tabs from overwriting each other's answers.
- Store immutable question snapshots per attempt, so future bank edits cannot change an old score. Deadline is an absolute browser timestamp; expired attempts settle on reopening.
- Answer explanations stay hidden in UI until submission. Static data includes answer keys; this is a self-study site, not an anti-cheating exam server.
- Vite relative base and one asset helper handle arbitrary repository names, custom domains and local preview.
- GitHub Actions builds/uploads dist and deploys to Pages after push to main. Original files under slides/ remain unchanged.

## Tasks

- [x] G01: tests and static export for data/PDF assets; validate published paths and original hashes.
- [x] G02: tested browser service and atomic IndexedDB persistence for practice, deadlines, grading, flags and retry.
- [x] G03: switch default app to browser storage, fix source/image/PDF paths under repo prefixes, preserve UI and error recovery.
- [x] G04: GitHub Pages workflow, ignores, portable static preview and exact push/deploy instructions.
- [x] G05: unit tests, build, API-free browser tests under a repo subpath, all modules and independent final review.

## Verification

Unit: reload persistence, expired/immutable attempts, idempotency, insufficient pools, no source/keys in active views, immutable snapshots, save failure, atomic concurrent updates, site-relative paths. Browser: no /api requests, practice and refresh, 50-question exam/flags/change/submit/retry, timer, source images/PDFs, isolation across contexts, 36 modules, narrow viewport. Build on a case-sensitive CI checkout must include data, PDFs and local fonts and must not include .local/user progress.

Verified 2026-11-22: 18/18 unit tests, validator zero errors and original hashes unchanged, production build, 8/8 static browser tests under /pages-proof/. Independent review found stale pre-transaction clock capture; failing regression added then fixed by capturing time inside transaction. No remote push/publication performed. Academic full-source review remains pending.
