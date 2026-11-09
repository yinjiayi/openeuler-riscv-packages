# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-longstring
Version:        0.17
Release:        1%{?dist}
Summary:        Perl assertions for comparing long strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test-LongString
Source0:        https://cpan.metacpan.org/authors/id/R/RG/RGARCIA/Test-LongString-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::Builder) >= 0.12
BuildRequires:  perl(Test::Builder::Tester) >= 1.04
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(Devel::Symdump)
BuildRequires:  perl(Pod::Parser)
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(Test::Builder) >= 0.12
Requires:       perl(Test::Builder::Tester) >= 1.04
Requires:       perl(Test::More)

%description
Compare long strings with focused diagnostics for exact equality, regular
expression matches, substrings and common text.

%prep
%setup -q -n Test-LongString-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
perl -MTest::Pod -MTest::Pod::Coverage -e '1'
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Test/LongString.pm
%{_mandir}/man3/Test::LongString.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Package the fixed upstream release and retain its complete default tests.
