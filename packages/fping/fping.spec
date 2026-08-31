# SPDX-License-Identifier: Apache-2.0
Name: fping
Version: 5.5
Release: 1%{?dist}
Summary: Send ICMP echo probes to network hosts in parallel
License: HPND-sell-variant
URL: https://fping.org/
Source0: fping-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: make

%description
fping sends ICMP echo probes to multiple hosts efficiently.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
./src/fping -v | grep -F '%{version}'
./src/fping -h >/dev/null
test "$(./src/fping -g 192.0.2.1 192.0.2.2 | wc -l)" -eq 2

%files
%license COPYING
%doc CHANGELOG.md README.md
%{_sbindir}/fping
%{_mandir}/man8/fping.8*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.5-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
