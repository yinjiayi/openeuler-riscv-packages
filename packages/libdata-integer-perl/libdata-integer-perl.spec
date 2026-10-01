# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Integer
Version:        0.007
Release:        1%{?dist}
Summary:        Native integer properties and operations for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Integer
Source0:        Data-Integer-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(constant)
BuildRequires:  perl(integer)
BuildRequires:  perl(parent)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Data::Integer exposes native signed and unsigned integer properties,
conversions, arithmetic and bitwise operations to Perl programs.

%prep
%autosetup -n Data-Integer-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all ten default upstream tests, including POD syntax and coverage.
%make_build test

%files
%doc README Changes SECURITY.md
%{perl_vendorlib}/Data/Integer.pm
%{_mandir}/man3/Data::Integer.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.007-1
- Package the official CPAN release with all ten default upstream tests.
