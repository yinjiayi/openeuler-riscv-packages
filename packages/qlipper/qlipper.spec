# SPDX-License-Identifier: Apache-2.0
Name:           qlipper
Version:        6.1.0
Release:        1%{?dist}
Summary:        Lightweight & cross-platform clipboard history applet based on Qt
License:        GPL-2.0-or-later
URL:            https://github.com/pvanek/qlipper
Source0:        qlipper-6.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Lightweight & cross-platform clipboard history applet based on Qt

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
%doc README
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
