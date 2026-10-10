# SPDX-License-Identifier: Apache-2.0
Name:           lightdm-gtk-greeter
Version:        2.0.9
Release:        1%{?dist}
Summary:        GTK+ greeter for LightDM
License:        GPL-3.0-or-later
URL:            https://github.com/Xubuntu/lightdm-gtk-greeter
Source0:        lightdm-gtk-greeter-2.0.9.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
GTK+ greeter for LightDM

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.9-1
- Initial openEuler RISC-V package from the full package inventory.
