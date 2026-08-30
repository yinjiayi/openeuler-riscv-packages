<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcap-ng

This directory packages libcap-ng `0.9.3` release `2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The frozen distribution snapshot contains Fedora 44 lineage for this component; the official upstream release feed, repository tag, source tree, license files, and exact archive SHA-256 were independently verified before onboarding.

No Fedora spec or AUR content was executed. Optional Python bindings, deprecated interfaces, and the separate eBPF-based cap-audit tool are not part of this base package; the core library, inspection utilities, upstream tests, and an installed-library smoke test remain enabled. Any source retrieval during the network-enabled target build remains pinned and SHA-256 verified before `rpmbuild` starts.

The riscv64 canary build for release `1` completed upstream tests with no errors, then failed while packaging a legacy `/etc/bash_completion.d` manifest path. Release `2` records the file at the upstream-installed `/usr/share/bash-completion/completions/libcap-ng.bash_completion` path; this package-local correction does not disable tests or remove the completion feature.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
