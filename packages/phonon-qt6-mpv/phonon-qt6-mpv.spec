# SPDX-License-Identifier: Apache-2.0
Name:           phonon-qt6-mpv
Version:        0.1.0
Release:        1%{?dist}
Summary:        Phonon MPV backend for Qt6
License:        LGPL-2.1-or-later
URL:            https://github.com/OpenProgger/phonon-mpv
Source0:        phonon-qt6-mpv-0.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Phonon MPV backend for Qt6

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license COPYING.LIB
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
