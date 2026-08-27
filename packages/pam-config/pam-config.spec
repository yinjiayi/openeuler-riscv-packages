# SPDX-License-Identifier: Apache-2.0
Name:           pam-config
Version:        2.14
Release:        1%{?dist}
Summary:        Utility to modify common PAM configuration files
License:        GPL-2.0-or-later
URL:            https://github.com/SUSE/pam-config
Source0:        pam-config-2.14.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Utility to modify common PAM configuration files

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
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.14-1
- Initial openEuler RISC-V package from the full package inventory.
