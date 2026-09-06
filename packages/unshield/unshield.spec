# SPDX-License-Identifier: Apache-2.0
Name:           unshield
Version:        1.6.2
Release:        3%{?dist}
Summary:        Extracts CAB files from InstallShield installers
License:        MIT
URL:            https://github.com/twogood/unshield
Source0:        unshield-1.6.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  zlib-devel

%description
Extracts CAB files from InstallShield installers

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) \
    ! -path '%{buildroot}%{_mandir}/man1/unshield.1' \
    -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%{_mandir}/man1/unshield.1*
%license LICENSE
%doc README.md
%doc ChangeLog

%changelog
* Sun Sep 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.2-3
- Declare the manual page separately so RPM's man-page compression is reflected in the file manifest.

* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.2-2
- Add the Zlib development files required by CMake.
- Configure the explicit CMake source and build directories.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.2-1
- Initial openEuler RISC-V package from the full package inventory.
