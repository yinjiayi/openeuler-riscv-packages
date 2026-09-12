# SPDX-License-Identifier: Apache-2.0
Name:           shmux
Version:        1.0.3
Release:        4%{?dist}
Summary:        shmux - executing the same command on many hosts in parallel.
License:        BSD-3-Clause
URL:            https://github.com/shmux/shmux
Source0:        shmux-1.0.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pcre-devel

%description
shmux - executing the same command on many hosts in parallel.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ulimit -n 1024
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-4
- Route the complete signal- and timer-sensitive test suite to native RISC-V.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-3
- Bound the test file-descriptor limit to avoid a QEMU-amplified close loop.
- Keep all upstream command, analyzer, exit-code, and timer tests enabled.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-2
- Declare terminal and PCRE development dependencies and run the upstream test target.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
