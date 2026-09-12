# SPDX-License-Identifier: Apache-2.0
Name:           teg
Version:        0.13.0
Release:        4%{?dist}
Summary:        Tenes Empanadas Graciela (TEG) is a clone of a 'Plan Tactico y Estrategico de la Guerra' board game, a pseudo-clone of Risk, a multiplayer turn-based strate
License:        GPL-2.0-or-later
URL:            https://github.com/wfx/teg
Source0:        teg-0.13.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext-devel
BuildRequires:  glib2-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  make

%description
Tenes Empanadas Graciela (TEG) is a clone of a 'Plan Tactico y Estrategico de la Guerra' board game, a pseudo-clone of Risk, a multiplayer turn-based strate

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13.0-4
- Add the libxml2 development dependency required by configure.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13.0-3
- Add the GLib development macros required by autoreconf.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13.0-2
- Add the gettext development tools required by autoreconf.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13.0-1
- Initial openEuler RISC-V package from the full package inventory.
