# SPDX-License-Identifier: Apache-2.0
Name:           perl-Math-Expression-Evaluator
Version:        0.3.2
Release:        1%{?dist}
Summary:        Parse and evaluate mathematical expressions in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Expression-Evaluator
Source0:        Math-Expression-Evaluator-v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Math::Trig)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)
Requires:       perl(Math::Trig)

%description
Math::Expression::Evaluator parses, compiles and evaluates mathematical
expressions with variables, built-in functions and optimization.

%prep
%autosetup -n Math-Expression-Evaluator-v%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all upstream default tests, including POD and POD coverage.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Math/Expression/Evaluator.pm
%{perl_vendorlib}/Math/Expression/Evaluator/
%{perl_vendorlib}/Math/Expression/benchmark.pl
%{_mandir}/man3/Math::Expression::Evaluator*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-1
- Package the official CPAN release with its complete default test suite.
