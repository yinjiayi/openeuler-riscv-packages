<!-- SPDX-License-Identifier: Apache-2.0 -->
# tpm2-tss

This directory packages upstream `https://github.com/tpm2-software/tpm2-tss` version `4.1.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `2` declares the official Autoconf Archive, pkg-config, OpenSSL, JSON-C, libcurl, and UUID development providers required by the default build and enables upstream's cmocka unit tests with the actual `--enable-unit` configure option. Integration tests remain at their upstream default because they require a TPM simulator and additional integration infrastructure; no library or TCTI feature is disabled, the source SHA-256 is unchanged, and the RISC-V build status remains `unknown` pending fresh CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
