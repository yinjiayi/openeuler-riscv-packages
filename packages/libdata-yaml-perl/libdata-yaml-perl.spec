# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-YAML
Version:        0.0.7
Release:        1%{?dist}
Summary:        Lightweight YAML serialization of Perl data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-YAML
Source0:        Data-YAML-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(version)
BuildRequires:  perl-generators

%description
Data::YAML provides a lightweight reader and writer for a subset of YAML,
focused on round-tripping Perl data structures.

%prep
%autosetup -n Data-YAML-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all seven unchanged upstream default tests, including both POD suites.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Data/YAML.pm
%{perl_vendorlib}/Data/YAML/
%{_mandir}/man3/Data::YAML*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.7-1
- Package the official CPAN release with its complete default test suite.
