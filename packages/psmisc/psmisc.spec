# SPDX-License-Identifier: Apache-2.0
Name:           psmisc
Version:        23.7
Release:        1%{?dist}
Summary:        Utilities for managing processes
License:        GPL-2.0-or-later
URL:            https://gitlab.com/psmisc/psmisc
Source0:        psmisc-%{version}.tar.xz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  dejagnu
BuildRequires:  expect
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libselinux-devel
BuildRequires:  make
BuildRequires:  ncurses-devel

%description
psmisc supplies process-management utilities including pstree, killall, fuser,
prtstat, and pslog.

%prep
%autosetup -p1

%build
%configure --enable-selinux
%make_build

%install
%make_install
%if "%{_sbindir}" != "%{_bindir}"
install -d %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/fuser %{buildroot}%{_sbindir}/fuser
%endif
%find_lang %{name} --all-name --with-man

%check
%make_build check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog README
%{_sbindir}/fuser
%{_bindir}/killall
%{_bindir}/prtstat
%{_bindir}/pslog
%{_bindir}/pstree
%{_bindir}/pstree.x11
%{_mandir}/man1/fuser.1*
%{_mandir}/man1/killall.1*
%exclude %{_mandir}/man1/peekfd.1*
%{_mandir}/man1/prtstat.1*
%{_mandir}/man1/pslog.1*
%{_mandir}/man1/pstree.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 23.7-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
