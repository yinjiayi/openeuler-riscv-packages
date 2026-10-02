# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Float
Version:        0.015
Release:        1%{?dist}
Summary:        Inspect and manipulate Perl floating-point values
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Float
Source0:        Data-Float-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Data::Float inspects Perl's native floating-point values and supplies
classification, conversion, comparison and neighboring-value operations.

%prep
%autosetup -n Data-Float-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all ten default upstream files without dropping floating-point cases.
%make_build test

%files
%license README
%doc Changes SECURITY.md
%{perl_vendorlib}/Data/Float.pm
%{_mandir}/man3/Data::Float.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.015-1
- Package the official CPAN release with all ten default upstream tests.
