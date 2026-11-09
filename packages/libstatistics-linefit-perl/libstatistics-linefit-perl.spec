# SPDX-License-Identifier: Apache-2.0
Name:           libstatistics-linefit-perl
Version:        0.07
Release:        1%{?dist}
Summary:        Fit a straight line to weighted or unweighted data in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Statistics-LineFit
Source0:        Statistics-LineFit-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::Simple) >= 0.44
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(Carp)

%description
Fit a straight line to weighted or unweighted data in Perl and query the
coefficients, predicted values, residuals, and related fit statistics.

%prep
%setup -q -n Statistics-LineFit

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Statistics/LineFit.pm
%{_mandir}/man3/Statistics::LineFit.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package the pinned upstream release and run its unchanged tests.
