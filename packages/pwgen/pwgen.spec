# SPDX-License-Identifier: Apache-2.0
Name:           pwgen
Version:        2.08
Release:        1%{?dist}
Summary:        Generate memorable or secure passwords
License:        GPL-2.0-only
URL:            https://sourceforge.net/projects/pwgen/
Source0:        pwgen-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
pwgen generates passwords that are designed to be easily memorized or, with
secure mode enabled, passwords made from cryptographically random characters.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
./pwgen -s -1 16 4 | \
  awk 'length($0) != 16 { exit 1 } END { if (NR != 4) exit 1 }'
printf 'openEuler-riscv64-RVA23\n' > check-seed
first=$(./pwgen -H "$PWD/check-seed#b19" -1 16 3)
second=$(./pwgen -H "$PWD/check-seed#b19" -1 16 3)
test "$first" = "$second"
printf '%s\n' "$first" | \
  awk 'length($0) != 16 { exit 1 } END { if (NR != 3) exit 1 }'

%files
%license debian/copyright
%{_bindir}/pwgen
%{_mandir}/man1/pwgen.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.08-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
