# SPDX-License-Identifier: Apache-2.0
Name:           graftcp
Version:        0.8.2
Release:        1%{?dist}
Summary:        A flexible tool for redirecting a program's TCP, UDP, and DNS traffic to SOCKS5 or HTTP proxies.
License:        GPL-3.0-or-later
URL:            https://github.com/hmgle/graftcp
Source0:        graftcp-0.8.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A flexible tool for redirecting a program's TCP, UDP, and DNS traffic to SOCKS5 or HTTP proxies.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.2-1
- Initial openEuler RISC-V package from the full package inventory.
