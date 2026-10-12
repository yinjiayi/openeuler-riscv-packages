# SPDX-License-Identifier: Apache-2.0
Name:           sandbox
Version:        2.46
Release:        1%{?dist}
Summary:        Gentoo sandbox tool and library
License:        GPL-2.0-or-later
URL:            https://github.com/gentoo/sandbox
Source0:        sandbox-2.46.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Gentoo sandbox tool and library

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.46-1
- Initial openEuler RISC-V package from the full package inventory.
