# SPDX-License-Identifier: Apache-2.0
Name:           fql
Version:        1.2.0
Release:        1%{?dist}
Summary:        A SQL interpreter for text processing
License:        MIT
URL:            https://github.com/jasonKercher/fql
Source0:        fql-1.2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A SQL interpreter for text processing

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
