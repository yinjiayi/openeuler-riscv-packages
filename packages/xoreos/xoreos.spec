# SPDX-License-Identifier: Apache-2.0
Name:           xoreos
Version:        0.0.6
Release:        4%{?dist}
Summary:        A reimplementation of BioWare's Aurora engine
License:        GPL-3.0-or-later
URL:            https://github.com/xoreos/xoreos
Source0:        xoreos-0.0.6.tar.gz
BuildRequires:  boost-date-time
BuildRequires:  boost-devel
BuildRequires:  boost-filesystem
BuildRequires:  boost-locale
BuildRequires:  boost-system
BuildRequires:  cmake
BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  openal-soft-devel
BuildRequires:  SDL2-devel
BuildRequires:  zlib-devel

%description
A reimplementation of BioWare's Aurora engine

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
cmake --build %{_vpath_builddir} --target check %{?_smp_mflags} --verbose

%files -f %{name}.files
%license COPYING
%doc README.md
%doc NEWS.md
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.6-4
- Build and run the upstream check target so excluded test binaries exist.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.6-3
- Raise the bounded QEMU build timeout to 180 minutes after exact-head CI
  compiled normally to 44% before the 60-minute package budget expired.

* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.6-2
- Add the official development packages required by the CMake configuration.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
