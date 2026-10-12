# SPDX-License-Identifier: Apache-2.0
Name:           knfmt
Version:        5.3.1
Release:        1%{?dist}
Summary:        C code formatter (OpenBSD KNF, limited .clang-format support)
License:        ISC
URL:            https://github.com/mptre/knfmt
Source0:        knfmt-5.3.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
C code formatter (OpenBSD KNF, limited .clang-format support)

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
