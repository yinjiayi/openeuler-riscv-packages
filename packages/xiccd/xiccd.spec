# SPDX-License-Identifier: Apache-2.0
Name:           xiccd
Version:        0.4.1
Release:        1%{?dist}
Summary:        X color profile daemon
License:        GPL-3.0-or-later
URL:            https://github.com/agalakhov/xiccd
Source0:        xiccd-0.4.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
X color profile daemon

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
