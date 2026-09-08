# SPDX-License-Identifier: Apache-2.0
Name:           dateutils
Version:        0.4.11
Release:        1%{?dist}
Summary:        Command-line tools for fast date and time calculations
License:        BSD-3-Clause
URL:            https://github.com/hroptatyr/dateutils
Source0:        dateutils-%{version}.tar.xz

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gperf
BuildRequires:  make
BuildRequires:  texinfo
BuildRequires:  tzdata

%description
dateutils provides command-line tools for date and time arithmetic,
conversion, sequencing, sorting, testing, and time-zone operations.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
# RPM owns the Info index globally, and %license installs the authoritative
# copy under %{_licensedir}; do not retain upstream's duplicate doc copy.
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE

%check
%make_build check

%files
%license LICENSE
%doc README.md
%{_bindir}/dateadd
%{_bindir}/dateconv
%{_bindir}/datediff
%{_bindir}/dategrep
%{_bindir}/dateround
%{_bindir}/dateseq
%{_bindir}/datesort
%{_bindir}/datetest
%{_bindir}/datezone
%{_bindir}/dadd
%{_bindir}/dconv
%{_bindir}/ddiff
%{_bindir}/dgrep
%{_bindir}/dround
%{_bindir}/dseq
%{_bindir}/dsort
%{_bindir}/dtest
%{_bindir}/dzone
%{_bindir}/strptime
%{_datadir}/dateutils/
%{_infodir}/dateutils.info*
%{_mandir}/man1/*.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.11-1
- Initial openEuler RISC-V package with the complete upstream Automake gate.
