# SPDX-License-Identifier: Apache-2.0
Name:           textparser
Version:        1.0.5
Release:        1%{?dist}
Summary:        Flexible and eazy to integrate text parser library written in C.
License:        MIT
URL:            https://github.com/bokic/textparser
Source0:        textparser-1.0.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Flexible and eazy to integrate text parser library written in C.

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.5-1
- Initial openEuler RISC-V package from the full package inventory.
