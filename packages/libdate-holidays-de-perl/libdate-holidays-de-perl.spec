# SPDX-License-Identifier: Apache-2.0
Name:           libdate-holidays-de-perl
Version:        2.07
Release:        1%{?dist}
Summary:        Calculate German holiday dates by year and state
License:        ISC
URL:            https://metacpan.org/dist/Date-Holidays-DE
Source0:        Date-Holidays-DE-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Date::Calc) >= 5.0
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test)
Requires:       perl
Requires:       perl(Date::Calc) >= 5.0
Requires:       perl(POSIX)
Requires:       perl(Time::Local)
Requires:       perl(Exporter)

%description
Date::Holidays::DE returns calculated German holiday dates for a
specified year and federal state, with configurable date formatting.

%prep
%autosetup -n Date-Holidays-DE-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Run the original default test.pl unchanged.
make test TEST_VERBOSE=1

%files
%license README
%doc Changes
%{perl_vendorlib}/Date/Holidays/DE.pm
%{_mandir}/man3/Date::Holidays::DE.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.07-1
- Package the official CPAN release and run the original default test.
