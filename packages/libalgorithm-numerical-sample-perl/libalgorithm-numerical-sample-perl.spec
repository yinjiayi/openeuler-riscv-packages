# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Numerical-Sample
Version:        2010011201
Release:        1%{?dist}
Summary:        Random sampling from finite and streamed sets in Perl
License:        MIT
URL:            https://metacpan.org/dist/Algorithm-Numerical-Sample
Source0:        Algorithm-Numerical-Sample-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-NoWarnings
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Algorithm::Numerical::Sample draws a random subset from a finite set or
a stream of values.

%prep
%autosetup -n Algorithm-Numerical-Sample-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all four upstream t/ files with POD, coverage, and warning dependencies
# installed, so their optional assertions are not silently skipped.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Algorithm/Numerical/Sample.pm
%{_mandir}/man3/Algorithm::Numerical::Sample.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2010011201-1
- Package the official CPAN release and complete default test suite.
