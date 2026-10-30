# SPDX-License-Identifier: Apache-2.0
Name:           perl-HTML-CalendarMonthSimple
Version:        1.27
Release:        1%{?dist}
Summary:        Generate HTML month calendars
License:        BSD-3-Clause
URL:            https://metacpan.org/release/HTML-CalendarMonthSimple
Source0:        HTML-CalendarMonthSimple-1.27.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Simple)
BuildRequires:  perl(Date::Calc)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl
Requires:       perl(Date::Calc)

%description
Generate HTML month calendars

%prep
%autosetup -p1 -n HTML-CalendarMonthSimple-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc README.md Changes
%{perl_vendorlib}/HTML/CalendarMonthSimple.pm
%{_mandir}/man3/HTML::CalendarMonthSimple.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.27-1
- Package HTML::CalendarMonthSimple with its original tests.
