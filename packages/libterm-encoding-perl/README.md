<!-- SPDX-License-Identifier: Apache-2.0 -->
# libterm-encoding-perl

This directory packages [Term::Encoding 0.03](https://metacpan.org/release/MIYAGAWA/Term-Encoding-0.03) for openEuler 24.03 LTS SP3 on `riscv64`/RVA23 as `perl-term-encoding`. The frozen Debian stable entry establishes discovery lineage; the fixed CPAN archive, verified against the publisher's metadata and PAUSE signature, is the only build source.

The unchanged upstream suite runs with the original developer and author guards. The installed check exercises both the native locale lookup and a deterministic locale-environment fallback. No architecture patch is needed.

The original license contains both Perl terms in full and the module retains the upstream author notices. The generated Makefile and original guarded POD test match Ricardo SIGNES's Dist::Zilla 6.012 templates; their complete terms match the originals apart from author notices, so the package carries separate precise template attribution without installing the helper code.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
