# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Sorting
Version:        0.9
Release:        1%{?dist}
Summary:        Multi-key sorting of Perl data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Sorting
Source0:        Data-Sorting-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators

%description
Data::Sorting supplies functions for sorting arrays and other Perl data
structures by multiple keys or calculated comparison values.

%prep
%autosetup -n Data-Sorting-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all seven default upstream test files and their bundled helper.
%make_build test

%files
%license README
%doc CHANGES
%{perl_vendorlib}/Data/Sorting.pm
%{_mandir}/man3/Data::Sorting.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9-1
- Package the official CPAN release with its unchanged default test suite.
