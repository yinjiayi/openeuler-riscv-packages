# SPDX-License-Identifier: Apache-2.0
Name:           sipsak
Version:        0.9.8.1
Release:        1%{?dist}
Summary:        Command-line SIP testing utility
License:        GPL-2.0-only
URL:            https://github.com/nils-ohlmeier/sipsak
Source0:        sipsak-0.9.8.1.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  check-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig

%description
sipsak is a command-line utility for testing SIP applications and servers.

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
./sipsak --version | grep -F '%{version}'

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/sipsak
%{_mandir}/man1/sipsak.1*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.8.1-1
- Initial openEuler RISC-V package.

