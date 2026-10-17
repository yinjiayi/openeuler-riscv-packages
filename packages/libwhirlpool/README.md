# libwhirlpool 1.1

Canonical upstream is dfateyev/libwhirlpool, official stable v1.1, commit
`b7721a44275793171c4b8ee17645394d9b5c927e`. The fixed HTTPS archive SHA-256 is
`b05c8fbc3fb6059e9f035b1354d8c8c4514f7cba84393292efce59181dcbac5d`;
all 33 files were checked against the complete upstream Git tree. Fedora
1.1-11.fc44 in discovery snapshot discovery-20260808T165000Z-9a89920c269462cd
is retained as lineage only, not executable source evidence. The snapshot's
unverified-source hold is resolved by the fixed official tag/archive above.

The original COPYING/README grant places this implementation in the public
domain with express redistribution permission. `LicenseRef-Public-Domain`
denotes that exact retained grant, not the different full Unlicense text.
Original per-file notices, X Consortium install-sh notice, unlimited-copy m4
notices and source-only GNU helper GPL2+/GPL3+ notices/additional permissions
remain unchanged. Complete official GPL2/GPL3 texts accompany those helpers.
The Apache2 packaging/consumer fixture has its complete license supplied;
none of this relicenses the original library or GNU helpers.

Target: only locked openEuler 24.03 LTS SP3 riscv64/RVA23, offline build after
verified source/dependency preparation. Original generated configure/config.sub
already recognize riscv64. No architecture shortcut, bundled
dependency download, feature removal or local upstream/RPM/QEMU execution.
Default shared/static libraries and CLI/man page are retained. Fresh complete
official and supplemental primary/filelists joins found no package, SONAME or
owned-file collision and no missing declared build/tooling dependency; this is
inventory evidence, not a substitute for CI's actual DNF resolution.

One downstream correctness patch fixes a reviewed one-byte out-of-bounds write
in check-mode digest termination: a 129-byte allocation's cursor already points
at byte 128, so terminate there instead of byte 129. It does not change checksum
comparison, exit status or original tests. This is a generic source bug, not a
claimed RISC-V defect. No upstream write was made. Remove the patch when a fixed
official release contains the same correction and the unchanged tests pass.

Original `make check` is retained (no registered suite in this release), and
the original `whirlpoolsum --test` API routine is executed in both %check and
installed smoke. Because that routine returns void even on failure, acceptance
requires `No error detected.` and rejects every `API error`, not just exit 0.
No original command/assertion is disabled. Separately, downstream consumers
verify empty/abc known answers with segmented input against staged and installed
shared/static interfaces. These constants are corroborated by official OpenSSL
3.0.0 commit `89cd17a031e022211684eb7eb41190cf1910f9fa`,
`test/recipes/30-test_evp_data/evpmd_whirlpool.txt` (ISO vector set;
Copyright 2001-2020 The OpenSSL Project Authors. All Rights Reserved., Apache2).
Installed CLI verification accepts the correct abc file and must reject a changed
file with exit 1 and `input: FAILED`. These are correctness tests, not native
RISC-V performance measurements, cryptographic certification or security approval.

Before merge require fresh exact-head full required CI, original tests, actual
target RPM build/install, schema-valid results, source/legal/ELF and physical
RPM/SRPM inspection. Hosted PR runs never use the self-hosted pool. Publication
is independently accepted against immutable metadata and real public products;
neither a submitted PR nor a passed tooling test implies target/native success.
