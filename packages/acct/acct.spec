# SPDX-License-Identifier: Apache-2.0
Name:           acct
Version:        6.6.4
Release:        1%{?dist}
Summary:        User-Specific Process Accounting
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/acct/
Source0:        acct-6.6.4.tar.bz2
BuildRequires:  gcc
BuildRequires:  make


%description
User-Specific Process Accounting

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*
%{_sbindir}/accton
%{_sbindir}/dump-acct
%{_sbindir}/dump-utmp
%{_sbindir}/sa
%{_infodir}/accounting.info*
%{_mandir}/man1/ac.1*
%{_mandir}/man1/last.1*
%{_mandir}/man1/lastcomm.1*
%{_mandir}/man8/accton.8*
%{_mandir}/man8/dump-acct.8*
%{_mandir}/man8/dump-utmp.8*
%{_mandir}/man8/sa.8*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.6.4-1
- Initial openEuler RISC-V package from the full package inventory.
