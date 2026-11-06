# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Fibonacci
Version:        1.5
Release:        1%{?dist}
Summary:        Fibonacci sequence functions for Perl
License:        Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Fibonacci
Source0:        Math-Fibonacci-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Math::Fibonacci provides sequence terms, series, number decomposition and
sequence membership checks for Perl.

%prep
%autosetup -n Math-Fibonacci-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both original t/*.t files with the original 19 assertions intact.
%make_build test

%files
%license ARTISTIC
%doc Changes TODO
%{perl_vendorlib}/Math/Fibonacci.pm
%{_mandir}/man3/Math::Fibonacci.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5-1
- Package official CPAN release with complete default tests.
