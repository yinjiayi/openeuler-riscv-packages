# SPDX-License-Identifier: Apache-2.0
Name:           wdiff
Version:        1.2.3
Release:        2%{?dist}
Summary:        Display word differences between text files
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/wdiff/
Source0:        wdiff-1.2.3.tar.gz

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  screen
BuildRequires:  sed
BuildRequires:  texinfo
BuildRequires:  which
Requires:       diffutils

%description
GNU wdiff compares two text files and reports deleted and inserted words. It
uses GNU diff to identify changed regions and then presents the changes at
word granularity.

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
%doc AUTHORS BACKLOG ChangeLog NEWS README THANKS TODO
%{_bindir}/wdiff
%{_infodir}/wdiff.info*
%{_mandir}/man1/wdiff.1*
%{_datadir}/locale/*/LC_MESSAGES/wdiff*.mo

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.3-2
- Make the installed smoke version check follow the packaged RPM version.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.2-1
- Initial openEuler RISC-V package with the complete upstream test suite.
