# Working Log

## 2026-07-10

- Added `innovation-assistant-skill` to the public skill ecosystem as the Innovation capability for structured innovation pipelines (SIT + Think Bigger).

## 2026-06-06

- Added `google-maps-routing-skill` to the public skill ecosystem as the Maps / travel capability for Google Maps Routes + Geocoding CLI workflows.
- Updated README, setup guide, and starter skill index examples so Google Maps appears alongside other standalone public skill repos.

## 2026-05-25

- Moved image generation from built-in skill (`rules/skills/generate_image.md`, `tools/generate_image.py`) to independent public repo [`image-generation-skill`](https://github.com/grapeot/image-generation-skill). The starter repo now references it via `docs/SKILL_ECOSYSTEM.md` instead of shipping its own implementation.
- Removed `rules/skills/generate_image.md`, `tools/generate_image.py`, and `tools/tests/test_generate_image.py` from the starter set.
- Updated `rules/skills/INDEX.md` to point users to the ecosystem index for image generation.
- Added image-generation-skill row to `docs/SKILL_ECOSYSTEM.md`.

- Added three generic best-practice skills to the starter set: PDF-to-Markdown with Docling, GUI automation methodology, and product/technical decision reverse engineering.
- Redacted the PDF conversion skill's local report path so the public version stays workspace-neutral.

- Added a human- and agent-readable public skill ecosystem index at `docs/SKILL_ECOSYSTEM.md`.
- Linked the ecosystem index from `README.md`, `setup_guide.md`, and `rules/skills/INDEX.md` so users can discover standalone skill repos without loading every repo into the starter skill index.
- Kept the model as public repo + private workspace overlay: public repos hold generic CLI contracts and tests; local workspaces hold aliases, paths, endpoints, credentials, and business context.
- Updated `rules/skills/project_scaffold.md` with the public skill repo installation convention: loose Markdown-based install, one root/router skill per repo, and private overlays outside the public repo.
