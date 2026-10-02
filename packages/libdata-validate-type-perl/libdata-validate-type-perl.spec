# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Validate-Type
Version:        1.6.0
Release:        1%{?dist}
Summary:        Type validation functions for Perl data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Validate-Type
Source0:        Data-Validate-Type-v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dump)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util) >= 1.18
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::FailWarnings)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl-generators

Requires:       perl(Data::Dump)
Requires:       perl(Scalar::Util) >= 1.18

%description
Data::Validate::Type offers boolean checks, assertions, and filters for
common Perl data types.

%prep
%autosetup -n Data-Validate-Type-v%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all thirteen unchanged default t/*.t files recursively.
./Build test

%files
%license LICENSE
%doc Changes README.md examples
%{perl_vendorlib}/Data/Validate/Type.pm
%{_mandir}/man3/Data::Validate::Type.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.0-1
- Package the official CPAN release with its complete default test suite.
