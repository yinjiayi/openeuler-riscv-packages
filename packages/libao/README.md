<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libao

This directory packages Xiph's official libao 1.2.0 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The HTTPS tarball SHA-256
`03ad231ad1f9d64b52474392d63c31197b0bc7bd416e58b1c10a329a5ed89caf`
matches Xiph's published downloads checksum. All archive members remain
under one top-level directory with no absolute or parent-traversal paths.
Upstream code is GPL-2.0-or-later; Apache-2.0 covers the packaging files.

The package retains built-in null, WAV, AU and raw output and requires ALSA
and PulseAudio plugins to be built and installed. The upstream release
registers no automated tests, so `%make_build check` does not claim functional
coverage. The separate installed smoke test opens and plays through null and
WAV drivers without audio hardware, checks the WAV header, and verifies that
the ALSA/PulseAudio plugin files are present. Hardware playback and timing
remain `needs-native-RISC-V`, beyond QEMU-user evidence.

Frozen Fedora metadata is discovery lineage only; no distribution recipe is
executed. Passing PR CI does not imply RPM repository publication.
