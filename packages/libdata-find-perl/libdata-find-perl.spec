# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Find
Version:        0.03
Release:        1%{?dist}
Summary:        Search nested Perl data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Find
Source0:        Data-Find-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Test::More)

%description
Data::Find searches nested Perl arrays and hashes and returns paths to
matching values, including within cyclic data structures.

%prep
%autosetup -n Data-Find-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all four default upstream tests, including POD coverage.
./Build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Data/Find.pm
%{_mandir}/man3/Data::Find.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package the official CPAN release with all four default upstream tests.
