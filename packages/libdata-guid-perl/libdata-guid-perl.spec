# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-GUID
Version:        0.051
Release:        1%{?dist}
Summary:        Perl objects and helpers for globally unique identifiers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-GUID
Source0:        Data-GUID-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::UUID) >= 1.148
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Sub::Exporter) >= 0.90
BuildRequires:  perl(Sub::Install) >= 0.03
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.78
BuildRequires:  perl-generators

%description
Data::GUID supplies immutable GUID objects, format conversions and helper
functions backed by Data::UUID.

%prep
%autosetup -n Data-GUID-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all five default upstream tests without exclusions or assertion changes.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Data/GUID.pm
%{_mandir}/man3/Data::GUID.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.051-1
- Package the official CPAN release with its unchanged default test suite.
