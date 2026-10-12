# SPDX-License-Identifier: Apache-2.0
Name:           glyr
Version:        1.0.10
Release:        1%{?dist}
Summary:        Music metadata searchengine utility and library written in C
License:        LGPL-3.0-or-later
URL:            https://github.com/sahib/glyr
Source0:        glyr-1.0.10.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Music metadata searchengine utility and library written in C

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
%doc AUTHORS
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.10-1
- Initial openEuler RISC-V package from the full package inventory.
