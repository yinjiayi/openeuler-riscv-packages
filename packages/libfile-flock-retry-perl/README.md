<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-flock-retry-perl

This directory packages upstream `https://metacpan.org/dist/File-Flock-Retry` version `0.632` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The official fixed CPAN archive is pinned by SHA-256, corroborated by
PAUSE-signed CHECKSUMS and byte-identical Debian sid upstream bytes.
The original full LICENSE is preserved. The generated build/author
templates are traced to Dist-Zilla 6.017, Test-Compile 2.058, and
Test-Perl-Critic-Subset 3.001.005; the package preserves their authorship
and compatible Perl dual-license notice.

The unmodified default suite runs all five test files: five top-level
assertions and three intrinsic author-only file skips. The installed
smoke uses a private temporary directory and ordinary nonblocking flock;
it does not claim timing, privileged, or native-kernel validation.
