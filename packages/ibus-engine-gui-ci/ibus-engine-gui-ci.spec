# SPDX-License-Identifier: Apache-2.0
Name:           ibus-engine-gui-ci
Version:        1.0.0.20220118
Release:        1%{?dist}
Summary:        GUI CI for IBus engines
License:        LGPL-2.1-or-later
URL:            https://github.com/fujiwarat/ibus-engine-gui-ci
Source0:        ibus-engine-gui-ci-1.0.0.20220118.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
GUI CI for IBus engines

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0.20220118-1
- Initial openEuler RISC-V package from the full package inventory.
