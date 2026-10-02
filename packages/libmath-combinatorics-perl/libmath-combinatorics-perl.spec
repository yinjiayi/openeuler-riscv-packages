# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Combinatorics
Version:        0.09
Release:        1%{?dist}
Summary:        Combinations and permutations in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Combinatorics
Source0:        Math-Combinatorics-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl-Data-Dumper

%description
Math::Combinatorics provides iterators and functions for combinations,
permutations and related counting operations in Perl.

%prep
%autosetup -n Math-Combinatorics-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all three upstream default t files and their 25 assertions.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Math/Combinatorics.pm
%{_mandir}/man3/Math::Combinatorics.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package official CPAN release with complete default tests.
