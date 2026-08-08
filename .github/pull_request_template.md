<!-- SPDX-License-Identifier: Apache-2.0 -->
## Package operation

- Package ID:
- Operation: onboarding / stable update / infrastructure
- Official upstream component and homepage:
- Stable release version:
- Discovery source and snapshot ID:
- Source archive URL:
- SHA-256 (and signature evidence when available):
- License evidence:
- BuildRequires / Requires changes:
- RISC-V status and QEMU suitability:
- RISC-V patch provenance and removal condition, if any:

## Scope and evidence

- [ ] This PR changes exactly one `packages/<package-id>/` directory, or is a separately scoped infrastructure PR.
- [ ] The source is an official stable release/tag; it is not an AUR binary or executed `PKGBUILD`.
- [ ] All source digests are verified and all RISC-V patches live under this package's `patches/` directory.
- [ ] `tests/smoke.sh` validates useful package behavior and has not been disabled to obtain a pass.
- [ ] No automated upstream issue, PR, or comment was created.
- [ ] No Codex/OpenAI credential is used by GitHub Actions.

## CI and merge

Required checks run against openEuler 24.03 LTS SP3 `riscv64`/RVA23. GitHub Auto-merge may squash this PR with zero required approvals only after every required check for the latest head SHA succeeds and no blocking label is present. `needs-native-riscv` remains open until a future approved native runner validates it.

