# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Hash-WithDefaults
Version:        0.05
Release:        1%{?dist}
Summary:        Tied Perl hashes with case handling and inherited defaults
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-WithDefaults
Source0:        Hash-WithDefaults-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Pod-Coverage
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl

%description
Hash::WithDefaults implements tied hashes with configurable key casing and
ordered fallback hashes whose values remain visible as defaults.

%prep
%autosetup -n Hash-WithDefaults-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep every original test, including the available POD syntax/coverage checks.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Hash/WithDefaults.pm
%{_mandir}/man3/Hash::WithDefaults.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package official CPAN release with complete default tests.
