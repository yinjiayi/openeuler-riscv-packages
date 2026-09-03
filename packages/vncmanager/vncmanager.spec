# SPDX-License-Identifier: Apache-2.0
Name:           vncmanager
Version:        1.0.2
Release:        5%{?dist}
Summary:        Session manager for VNC
License:        MIT
URL:            https://github.com/openSUSE/vncmanager
Source0:        vncmanager-1.0.2.tar.gz
Patch0:         patches/0001-stream-include-cstdint.patch
BuildRequires:  boost-devel
BuildRequires:  boost-iostreams
BuildRequires:  boost-program-options
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gnutls-devel
BuildRequires:  make

%description
Session manager for VNC

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

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-5
- Include cstdint explicitly for GCC 14.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-4
- Configure the explicit out-of-source directory used by build, install, and check.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-3
- Add the GnuTLS development files required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-2
- Add the Boost headers and libraries required by CMake.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
