# SPDX-License-Identifier: Apache-2.0
Name:           perl-accessors
Version:        1.01
Release:        1%{?dist}
Summary:        Create Perl accessor methods at compile time
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/accessors
Source0:        accessors-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build >= 0.20
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
The accessors pragma generates simple methods at compile time. It provides
chained, classic, read-write and read-only accessors for hash-based objects.

%prep
%autosetup -n accessors-%{version}

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build

%install
%{__perl} Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__perl} Build test

%files
%license Build.PL META.yml
%doc Changes INSTALL README TODO
%{perl_vendorlib}/accessors.pm
%{perl_vendorlib}/accessors/
%{_mandir}/man3/accessors.3*
%{_mandir}/man3/accessors::*.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.01-1
- Package the official CPAN release and preserve the complete default test suite.
