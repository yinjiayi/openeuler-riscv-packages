# SPDX-License-Identifier: Apache-2.0
Name:           gtypist
Version:        2.10.1
Release:        1%{?dist}
Summary:        Universal typing tutor
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gtypist/
Source0:        gtypist-2.10.1.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel


%description
Universal typing tutor

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
%find_lang %{name}
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_datadir}/gtypist/
%{_infodir}/gtypist*.info*
%{_mandir}/man1/gtypist.1*
%{_mandir}/man1/typefortune.1*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.10.1-1
- Initial openEuler RISC-V package from the full package inventory.
