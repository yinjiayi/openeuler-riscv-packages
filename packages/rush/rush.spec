# SPDX-License-Identifier: Apache-2.0
Name:           rush
Version:        2.4
Release:        1%{?dist}
Summary:        GNU Restricted User Shell
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/rush/
Source0:        rush-2.4.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel


%description
GNU Restricted User Shell

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
%{_sbindir}/rush
%config(noreplace) %{_sysconfdir}/rush.rc
%{_infodir}/rush.info*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4-1
- Initial openEuler RISC-V package from the full package inventory.
