# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Record
Version:        0.02
Release:        1%{?dist}
Summary:        Configurable record splitting for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Record
Source0:        Data-Record-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Sub::Uplevel) >= 0.09
BuildRequires:  perl(Test::Exception) >= 0.21
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
Requires:       perl(Sub::Uplevel) >= 0.09

%description
Data::Record splits input into records with configurable separators and
exceptions for content that should remain together.

%prep
%autosetup -n Data-Record-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all four default upstream tests, including POD syntax and coverage.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/Data/Record.pm
%{_mandir}/man3/Data::Record.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package the official CPAN release with all four default upstream tests.
