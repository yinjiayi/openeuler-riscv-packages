# SPDX-License-Identifier: Apache-2.0
Name:           rank
Version:        0.1.1
Release:        1%{?dist}
Summary:        GNU sort reimplementation: byte-identical output, MSD radix sorting
License:        MIT
URL:            https://github.com/tenseleyFlow/rank
Source0:        rank-0.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
GNU sort reimplementation: byte-identical output, MSD radix sorting

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
