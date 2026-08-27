# SPDX-License-Identifier: Apache-2.0
Name:           qcsxcad
Version:        0.6.3
Release:        1%{?dist}
Summary:        Qt-GUI for CSXCAD
License:        LGPL-3.0-or-later
URL:            https://github.com/thliebig/QCSXCAD
Source0:        qcsxcad-0.6.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qt-GUI for CSXCAD

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3-1
- Initial openEuler RISC-V package from the full package inventory.
