# SPDX-License-Identifier: Apache-2.0
Name:           netperf
Version:        2.7.0
Release:        1%{?dist}
Summary:        Benchmarking tool for many different types of networking
License:        MIT
URL:            https://github.com/HewlettPackard/netperf
Source0:        netperf-2.7.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Benchmarking tool for many different types of networking

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
%license COPYING
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
