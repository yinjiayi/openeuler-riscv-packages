<!-- SPDX-License-Identifier: Apache-2.0 -->
# rf24

This directory packages upstream `https://github.com/nRF24/RF24` version `1.5.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release 2 selects the verified `RF24-1.5.0` archive root, builds the Linux SPIDEV driver, and explicitly installs the versioned library, ABI links, and public headers without running `ldconfig`. Upstream provides no automated tests, so the package check validates the real installed payload; radio hardware behavior is not claimed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
