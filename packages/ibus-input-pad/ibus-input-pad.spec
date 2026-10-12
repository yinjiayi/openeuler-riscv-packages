# SPDX-License-Identifier: Apache-2.0
Name:           ibus-input-pad
Version:        1.5.0
Release:        1%{?dist}
Summary:        Input Pad for IBus
License:        GPL-2.0-or-later
URL:            https://github.com/fujiwarat/ibus-input-pad
Source0:        ibus-input-pad-1.5.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Input Pad for IBus

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
