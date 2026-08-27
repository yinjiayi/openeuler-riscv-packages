# SPDX-License-Identifier: Apache-2.0
Name:           oplpctools
Version:        3.1
Release:        1%{?dist}
Summary:        Graphical PC tools for Open PS2 Loader (OPL)
License:        GPL-3.0-or-later
URL:            https://github.com/brainstream/OPL-PC-Tools
Source0:        oplpctools-3.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Graphical PC tools for Open PS2 Loader (OPL)

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1-1
- Initial openEuler RISC-V package from the full package inventory.
