# SPDX-License-Identifier: Apache-2.0
Name:           json-parser
Version:        1.1.0
Release:        1%{?dist}
Summary:        Very low footprint JSON parser written in portable ANSI C
License:        BSD-2-Clause
URL:            https://github.com/udp/json-parser
Source0:        json-parser-1.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Very low footprint JSON parser written in portable ANSI C

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
