<!-- SPDX-License-Identifier: Apache-2.0 -->
# liboauth

This directory packages liboauth `1.0.3` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official `v1.0.3` tag resolves to commit
`07fc30bf6d44f5b431a943452f6083fbaf22bc8f`; its immutable-commit HTTPS
archive has SHA-256
`d6ec68003262f62024f91f790de287802948df23d99939d982a6efce88251ce1`.
The archive is single-rooted, with only regular files and directories.

The compiled library selects upstream's MIT license. This build keeps libcurl
HTTP integration and OpenSSL-backed HMAC/RSA functionality; it does not select
the reduced built-in-hash mode. The package patch updates upstream's obsolete
EVP digest-context lifecycle for the target OpenSSL 3.0.12. The official
upstream README describes
`make check` as an offline self-test: all three registered tests (`tcwiki`,
`tceran`, `tcother`) run in `%check`, while network-dependent examples are
not registered. Installed-RPM smoke exercises the public URL escaping API
through the shipped pkg-config metadata.

Two target RISC-V CI runs (`36432105235` and `36433796200`) reported a
`tcwiki` segmentation fault after the HMAC assertions. A diagnostic run
(`36486701162`) retained the complete test and identified target NSS error
`-8011` (`SEC_ERROR_SIGNATURE_ALGORITHM_DISABLED`) for RSA-SHA1 signing.
Release 3 trials the existing upstream OpenSSL backend without changing the
system cryptographic policy or removing any test. The target CI must still
prove its build and runtime behavior; no RPM success is claimed here.

OpenSSL 3 is Apache-2.0-licensed. Upstream's MIT option permits this library
to be linked and distributed with it, while GPL-2.0-only downstream programs
may need separate compatibility review; upstream's exception covers its own
source, not every third-party consumer.

Fedora and Debian source-package metadata corroborate version and component
lineage. No downstream recipe was executed. MIT remains the upstream source
license; Apache-2.0 covers the original packaging metadata, test, and notes.
