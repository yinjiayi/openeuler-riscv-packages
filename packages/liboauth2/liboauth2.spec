# SPDX-License-Identifier: Apache-2.0
Name:           liboauth2
Version:        2.2.0
Release:        1%{?dist}
Summary:        Generic library to build OAuth 2.x and OpenID Connect servers and clients in C
License:        Apache-2.0
URL:            https://github.com/OpenIDC/liboauth2
Source0:        liboauth2-2.2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Generic library to build OAuth 2.x and OpenID Connect servers and clients in C

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
%license LICENSE
%doc README.md
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
