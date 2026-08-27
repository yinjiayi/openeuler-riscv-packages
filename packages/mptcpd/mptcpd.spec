# SPDX-License-Identifier: Apache-2.0
Name:           mptcpd
Version:        0.14
Release:        1%{?dist}
Summary:        Multipath TCP daemon
License:        BSD-3-Clause
URL:            https://github.com/multipath-tcp/mptcpd
Source0:        mptcpd-0.14.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Multipath TCP daemon

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-1
- Initial openEuler RISC-V package from the full package inventory.
