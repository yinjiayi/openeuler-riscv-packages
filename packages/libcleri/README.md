<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libcleri

This directory packages the official Cesbit libcleri 1.0.2 tag for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The v1.0.2 tag resolves to commit
`2964b6ce6ee57dac5d6dfd13f5a3a351c568fb2f`; its HTTPS archive SHA-256
is `7180ed1f215c30fba601a150ef9eb7a54f6efd4cf8f130bb4c5ed86ac03bc9c5`.
All archive members remain under `libcleri-1.0.2/`, with no absolute path,
parent traversal, or special-file type.

The frozen inventory combines two components under the libcleri name and
marks the discovery entry `license-blocked`. This package selects only the
official Cesbit component; its source `LICENSE.md` grants MIT terms. The
other component is not included. Apache-2.0 covers only the packaging files.

`%check` runs upstream's complete `Release` `make test` target, which invokes
`test/test.sh` over every `test_*` functional program. The script optionally
uses valgrind if available; valgrind coverage is not claimed when absent.
Installed smoke compiles and links a consumer against the packaged shared
library, verifying version and valid/invalid grammar parses. Passing QEMU-user
CI does not establish native RISC-V performance or repository publication.
