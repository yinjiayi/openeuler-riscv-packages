# SPDX-License-Identifier: Apache-2.0
Name:           mate-applet-lockkeys
Version:        0.4.0
Release:        1%{?dist}
Summary:        A MATE panel applet that shows which of the CapsLock, NumLock and ScrollLock keys are on and which are off.
License:        GPL-2.0-or-later
URL:            https://github.com/rezso/mate-applet-lockkeys
Source0:        mate-applet-lockkeys-0.4.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A MATE panel applet that shows which of the CapsLock, NumLock and ScrollLock keys are on and which are off.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
