# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Random-ISAAC
Version:        1.004
Release:        1%{?dist}
Summary:        Perl interface to the ISAAC pseudorandom number generator
License:        MIT
URL:            https://metacpan.org/dist/Math-Random-ISAAC
Source0:        Math-Random-ISAAC-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-LeakTrace
BuildRequires:  perl-Test-NoWarnings
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl

%description
Math::Random::ISAAC provides a Perl interface to the ISAAC pseudorandom
number generator, using its pure-Perl implementation when the optional XS
backend is unavailable.

%prep
%autosetup -n Math-Random-ISAAC-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the complete upstream default suite, including the available leak test.
%make_build test

%files
%license LICENSE README
%doc Changes
%{perl_vendorlib}/Math/Random/ISAAC.pm
%{perl_vendorlib}/Math/Random/ISAAC/PP.pm
%{_mandir}/man3/Math::Random::ISAAC.3*
%{_mandir}/man3/Math::Random::ISAAC::PP.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.004-1
- Package official CPAN release with complete default tests.
