# SPDX-License-Identifier: Apache-2.0
Name:           vtm
Version:        2026.07.30
Release:        3%{?dist}
Summary:        Terminal multiplexer with window manager and session sharing
License:        MIT
URL:            https://github.com/directvt/vtm
Source0:        vtm-2026.07.30.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  util-linux

%description
Terminal multiplexer with window manager and session sharing

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure
version_output=$(script --quiet --return --command '%{_vpath_builddir}/vtm --version' /dev/null </dev/null 2>&1)
printf '%%s\n' "$version_output"
printf '%%s\n' "$version_output" | grep -F -- 'v%{version}'

%files -f %{name}.files
%license LICENSE


%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2026.07.30-3
- Run version assertions through a pseudo-terminal while preserving child failures.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2026.07.30-2
- Allow 240 minutes for the large single-translation-unit QEMU build.
- Execute the built binary's version path in addition to upstream CTest discovery.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2026.07.30-1
- Initial openEuler RISC-V package from the full package inventory.
