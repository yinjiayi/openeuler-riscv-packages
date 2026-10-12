# SPDX-License-Identifier: Apache-2.0
Name:           perl-Math-Calc-Units
Version:        1.07
Release:        1%{?dist}
Summary:        Unit-aware calculator for Perl
License:        GPL-2.0-only OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Calc-Units
Source0:        Math-Calc-Units-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl-generators
Requires:       perl(Time::Local)

%description
Math::Calc::Units evaluates expressions and converts values while retaining
their physical units. It also installs the ucalc command-line calculator.

%prep
%autosetup -n Math-Calc-Units-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both unchanged default tests, including the optional POD test.
%make_build test

%files
%license LICENSE COPYING Artistic.html
%doc README Changes
%{_bindir}/ucalc
%{perl_vendorlib}/Math/Calc/Units.pm
%{perl_vendorlib}/Math/Calc/Units/
%{_mandir}/man3/Math::Calc::Units.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Package the official CPAN release and complete default tests.
