# SPDX-License-Identifier: Apache-2.0
Name:           vibestreamer
Version:        1.3.5
Release:        1%{?dist}
Summary:        Modern IPTV player with Xtream Codes and M3U support, built with Qt6 and libmpv
License:        MIT
URL:            https://github.com/krmmyvz/vibestreamer
Source0:        vibestreamer-1.3.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  zlib-devel

%description
Modern IPTV player with Xtream Codes and M3U support, built with Qt6 and libmpv

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.5-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the Qt 6, SVG, and zlib development files required by CMake.
