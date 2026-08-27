# SPDX-License-Identifier: Apache-2.0
Name:           sniproxy
Version:        0.7.0
Release:        1%{?dist}
Summary:        TLS SNI proxy
License:        BSD-2-Clause
URL:            https://github.com/dlundquist/sniproxy
Source0:        sniproxy-0.7.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  libev-devel
BuildRequires:  make
BuildRequires:  pcre2-devel

%description
TLS SNI proxy

%prep
%autosetup -p1

%build
autoreconf -fi
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
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.0-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the libev and PCRE2 development dependencies required by configure.
