# SPDX-License-Identifier: Apache-2.0
Name:           flacon
Version:        13.0.2
Release:        1%{?dist}
Summary:        An Audio File Encoder. Extracts audio tracks from an audio CD image to separate tracks.
License:        LGPL-2.1-or-later
URL:            https://github.com/flacon/flacon
Source0:        flacon-13.0.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  libxkbcommon-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  taglib-devel
BuildRequires:  uchardet-devel
BuildRequires:  zlib-devel

%description
An Audio File Encoder. Extracts audio tracks from an audio CD image to separate tracks.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 13.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the Qt 6, TagLib, and uchardet development files required by CMake.
- Add the XKB and zlib development files required by Qt and CMake.
