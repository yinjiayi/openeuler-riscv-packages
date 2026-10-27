<!-- SPDX-License-Identifier: Apache-2.0 -->
# gsm

This directory packages the official GSM 06.10 codec release `1.0.24` for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The official HTTPS tarball is
SHA-256 pinned to `a3c40c6471928383f4abfcb2e8f24012a1f562be2f17b8d672145d5986681a92`.
The single-rooted archive contains no unsafe paths or special members. Its
`COPYRIGHT` is the TU-Berlin-2.0 license.

The canonical `gsm` RPM contains `libgsm.so.1` and the toast family of tools;
`gsm-devel` contains the header, static archive, unversioned linker name,
manuals, and pkg-config metadata. This covers the discovered `libgsm` alias
without creating a conflicting second package. Upstream's Makefile targets
hard-coded paths and only builds a static library, so the spec builds PIC
objects, links a versioned shared library, and installs explicit file lists.

On LP64 RISC-V, C `long` is 64-bit, but GSM's internal `longword` arithmetic
requires 32 bits. The downstream patch changes those types to signed and
unsigned `int`, following upstream's documented 64-bit-long portability
guidance. Remove the patch when upstream adopts fixed-width 32-bit types.

Upstream's ETSI codec vectors are not distributed with this release; its
`tst/run` exits successfully without them and therefore cannot establish
conformance. `%check` instead runs the bundled arithmetic data, explicitly
fails on mismatch diagnostics, and exercises public encode/decode APIs.
Installed-RPM smoke repeats the API check against the shipped shared library
and pkg-config metadata. These tests are not a complete ETSI conformance suite.

The upstream source and downstream patch retain TU-Berlin-2.0 licensing;
Apache-2.0 covers the original packaging metadata, tests, and documentation.
