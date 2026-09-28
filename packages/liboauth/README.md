<!-- SPDX-License-Identifier: Apache-2.0 -->
# liboauth

This directory packages liboauth `1.0.3` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official `v1.0.3` tag resolves to commit
`07fc30bf6d44f5b431a943452f6083fbaf22bc8f`; its immutable-commit HTTPS
archive has SHA-256
`d6ec68003262f62024f91f790de287802948df23d99939d982a6efce88251ce1`.
The archive is single-rooted, with only regular files and directories.

The compiled library is MIT-licensed. This build keeps libcurl HTTP integration
and NSS-backed HMAC/RSA functionality; it does not select the reduced
built-in-hash mode. NSS is used because upstream's OpenSSL implementation
depends on obsolete context APIs. The official upstream README describes
`make check` as an offline self-test: all three registered tests (`tcwiki`,
`tceran`, `tcother`) run in `%check`, while network-dependent examples are
not registered. Installed-RPM smoke exercises the public URL escaping API
through the shipped pkg-config metadata.

Two target RISC-V CI runs (`36432105235` and `36433796200`) reported a
`tcwiki` segmentation fault after the HMAC assertions. Release 2 adds an NSS
error-code diagnostic and guards the RSA result comparison; the complete test
still fails if RSA signing fails. This is a diagnostic change, not evidence of
a successful RPM build or an NSS compatibility fix.

Fedora and Debian source-package metadata corroborate version and component
lineage. No downstream recipe was executed. MIT remains the upstream source
license; Apache-2.0 covers the original packaging metadata, test, and notes.
