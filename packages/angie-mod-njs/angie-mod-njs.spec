# SPDX-License-Identifier: Apache-2.0
Name:           angie-mod-njs
Version:        1.0.0
Release:        4%{?dist}
Summary:        nginScript module for angie
License:        BSD-2-Clause
URL:            https://github.com/nginx/njs
Source0:        angie-mod-njs-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pcre2-devel

%description
nginScript module for angie

%prep
%autosetup -p1 -n njs-%{version}

%build
./configure --ld-opt="%{build_ldflags}"
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
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-4
- Add the PCRE2 development dependency required by the njs configure checks.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-3
- Use the upstream shell configure interface while retaining RPM linker flags.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-2
- Enter the njs source archive's actual top-level directory during prep.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
