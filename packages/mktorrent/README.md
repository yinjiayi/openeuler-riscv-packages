# Mktorrent 1.1

The current Arch stable-extra entry delegates to `pobrn/mktorrent`. Official
stable tag `v1.1` resolves to full commit
`b20ef699b4ee5ded2f078ead776c7deac969e19a`. The exact GitHub-advertised archive
route is narrowed to that commit; the captured archive is 23,322 bytes with
SHA-256 `88b6336aca936c17c073bad7d4cb512470369c4ddbd240a680e25c66597efb61`.
All 19 archive entries (18 regular files) were inspected inertly. The captured
release has no assets and the original source documents advertise no detached
archive signature. No signature verification or exhaustive absence is claimed.

The original GNUmakefile/default `all` builds the prefix format probe and six
objects (`ftw`, `init`, `sha1`, `hash`, `output`, `main`). All upstream optional
switches remain unset: no pthread/OpenSSL/long-option feature is newly enabled
or disabled, and the redundant hash-byte check remains active. Normal install
places only the binary and does not strip it. RPM compiler/linker flags replace
only their corresponding supported Makefile variables. No patches are applied.

Upstream defines no default check/test target. Its original opt-in `SHA1_TEST`
code is unchanged and is additionally compiled/run against all three bundled
vectors in target `%check`. Authored deterministic fixtures run against built,
staged and installed binaries: single-file default piece length, multi-file
sorting and pieces crossing file boundaries, tracker tiers/web seeds/private
source/comment fields, missing/invalid arguments, and no-overwrite behavior.
No actual tracker or network endpoint is contacted. These checks are target-CI
requirements, not packaging-host execution or native/performance evidence.

The binary combines GPL-2.0-or-later code with explicitly public-domain SHA-1;
full original `COPYING` (including its OpenSSL exception) and both SHA-1 source
notices are retained. The tests package additionally contains MIT-authored QA
with its complete grant/disclaimer and the untouched full source archive.
`network_during_build:false` requests policy and is not proof of isolation;
actual build identity/network state and all target results require CI evidence.
