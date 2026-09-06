<!-- SPDX-License-Identifier: Apache-2.0 -->
# specgram

This directory packages upstream `https://github.com/rimio/specgram` version `0.9.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Exact-head Package CI run `33048339152` for commit
`2b33bad8ad17d611c7d3bcc61ffa3a5c11134f08` reached CMake configuration,
which requires SFML 2.5 or newer. Release 2 declares the required SFML and
FFTW development libraries together with GoogleTest and X11 for upstream's
test executable. Upstream names its test switch `TESTING`; the SPEC enables
that option, while the local CMake patch requires the test dependencies and
loads CMake's GoogleTest integration before upstream registers its tests. The
discovered tests remain under `%check`. The SFML dependency is supplied by the
separately reviewed SFML 2.x compatibility provider, so a fresh exact-head
target build remains required after that provider is published.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
