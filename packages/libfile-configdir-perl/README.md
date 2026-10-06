<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-configdir-perl

The frozen inventory's exact `libfile-configdir-perl` key maps to the latest
official [File-ConfigDir 0.021](https://metacpan.org/dist/File-ConfigDir).
The official CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have
SHA-256 `6b405a14f69ce49d4982ed9b75400a445d0f6224fd7687fb907e79c5578314c6`.
The 21 archive entries form one top-level tree without traversal paths, links
or special files. Bundled `LICENSE`, `GPL-1` and `ARTISTIC-1.0` explicitly
grant Perl dual-license terms, resolving the frozen automated
`unverified-upstream` decision for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-ConfigDir` nor `perl(File::ConfigDir)`; it does
contain the required `perl-Test-Without-Module` test dependency. This is a
snapshot check, not a guarantee about future repository state.

`%check` retains all six default upstream tests (60 assertions) including
loading, configuration directory discovery, plugin registration, missing
optional modules, internals and error handling. The upstream plugin test
creates and removes only a PID-named path inside the fresh CI source tree;
the simple test uses a temporary directory with cleanup. The installed-RPM
smoke registers a temporary configuration directory and verifies discovery.
The full upstream suite also passed locally on Perl 5.34.1; target
compatibility is not claimed until exact-head CI.

Successful PR CI artifacts alone do not prove public RPM repository publication.
