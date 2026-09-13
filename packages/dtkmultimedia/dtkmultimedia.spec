# SPDX-License-Identifier: Apache-2.0
Name:           dtkmultimedia
Version:        6.0.4
Release:        3%{?dist}
Summary:        Development Tool Kit Multimedia
License:        LGPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dtkmultimedia
Source0:        dtkmultimedia-6.0.4.tar.gz
BuildRequires:  cmake
BuildRequires:  ffmpeg-devel
BuildRequires:  gcc
BuildRequires:  libxkbcommon-devel
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtmultimedia-devel

%description
Development Tool Kit Multimedia

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.4-3
- Add the XKB, Qt Multimedia, and FFmpeg development dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.4-2
- Add the Qt 6 base development dependency required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.4-1
- Initial openEuler RISC-V package from the full package inventory.
