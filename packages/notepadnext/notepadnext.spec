# SPDX-License-Identifier: Apache-2.0
Name:           notepadnext
Version:        0.14
Release:        3%{?dist}
Summary:        Cross-platform reimplementation of Notepad++
License:        GPL-3.0-or-later
URL:            https://github.com/dail8859/NotepadNext
Source0:        notepadnext-0.14.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libxkbcommon-devel
BuildRequires:  make
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel

%description
Cross-platform reimplementation of Notepad++

%prep
%autosetup -n NotepadNext-%{version} -p1

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-3
- Add the XKB development files required by Qt 6 GuiPrivate.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-2
- Add the Qt6 LinguistTools development component required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-1
- Initial openEuler RISC-V package from the full package inventory.
