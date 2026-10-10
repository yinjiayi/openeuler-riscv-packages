# SPDX-License-Identifier: Apache-2.0
Name:           nodm
Version:        0.13
Release:        1%{?dist}
Summary:        X display manager for automatic logins
License:        GPL-2.0-or-later
URL:            https://github.com/spanezz/nodm
Source0:        nodm-0.13.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
X display manager for automatic logins

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Initial openEuler RISC-V package from the full package inventory.
