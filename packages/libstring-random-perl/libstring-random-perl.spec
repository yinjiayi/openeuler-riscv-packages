# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Random
Version:        0.32
Release:        1%{?dist}
Summary:        Generate random strings from character patterns
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Random
Source0:        String-Random-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Random generates strings matching character patterns or its
supported subset of regular-expression syntax. It uses Perl's rand
and must not be used to generate cryptographic secrets.

%prep
%autosetup -n String-Random-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all nine unmodified upstream default t/ files (202 assertions).
./Build test

%files
%license LICENSE
%doc Changes README README.md
%{perl_vendorlib}/String/Random.pm
%{_mandir}/man3/String::Random.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.32-1
- Package official CPAN release with all default upstream tests.
