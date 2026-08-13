# SPDX-License-Identifier: Apache-2.0
Name:           6tunnel
Version:        0.14
Release:        1%{?dist}
Summary:        IPv4 and IPv6 TCP proxy
License:        GPL-2.0-only
URL:            https://github.com/wojtekka/6tunnel
Source0:        6tunnel-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3

%description
6tunnel forwards TCP connections between IPv4 and IPv6 endpoints. It can bind
on either address family and connect to services available through the other.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install

%check
%make_build check
./6tunnel -V | grep -F '%{version}'

%files
%license COPYING
%doc ChangeLog README.md TODO
%{_bindir}/6tunnel
%{_mandir}/man1/6tunnel.1*

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-1
- Initial openEuler RISC-V package.
