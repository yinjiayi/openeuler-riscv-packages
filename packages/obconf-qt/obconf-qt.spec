# SPDX-License-Identifier: Apache-2.0
Name:           obconf-qt
Version:        0.16.6
Release:        1%{?dist}
Summary:        Openbox configuration tool. Qt port of ObConf
License:        GPL-2.0-or-later
URL:            https://github.com/lxqt/obconf-qt
Source0:        obconf-qt-0.16.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Openbox configuration tool. Qt port of ObConf

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
%license COPYING
%doc README.md
%doc AUTHORS
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16.6-1
- Initial openEuler RISC-V package from the full package inventory.
