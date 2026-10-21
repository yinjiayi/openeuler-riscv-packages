<!-- SPDX-License-Identifier: Apache-2.0 -->
# python-yaml

This directory packages PyYAML 6.0.3 for openEuler 24.03 LTS SP3 on
riscv64/RVA23, upgrading the fixed target's python3-pyyaml 6.0.1 build.

The frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd`
cross-checks Arch Extra 6.0.3-2, AUR pypy3-yaml metadata 6.0.3-1,
Fedora 44 6.0.3-3.fc44, Debian stable 6.0.2-1, openSUSE 6.0.3-1.6,
and Ubuntu Resolute 6.0.3-1build1. No AUR PKGBUILD or distribution
recipe was read or executed.

The source URL pins the official 6.0.3 tag's resolved full commit and
its SHA-256. The build forces the compiled LibYAML extension; it may not
silently fall back to the pure-Python implementation. The complete upstream
pytest collection runs against the buildroot-installed package, after a
separate assertion that `yaml.__with_libyaml__` is true.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts,
and documentation in this directory.
