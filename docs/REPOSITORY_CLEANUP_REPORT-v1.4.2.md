# Repository cleanup report — v1.4.2

Reviewed on 2026-07-17.

- `build/`, `dist/`, Python caches, coverage data, and logs are ignored and are
  not release source files.
- Versioned screenshots under `assets/screenshots/` remain source-controlled
  documentation assets; no broad screenshot deletion was performed.
- `README_EN.md` was already removed in favour of the canonical `README.md`.
- No Apple PingFang, Noto, HarmonyOS Sans, or unlicensed font file is present
  in the repository.
- Existing historical build logs and older screenshots were retained because
  their current references have not been exhaustively proven absent.

No untracked user files were deleted during this review.
