# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Faker
Version:        0.10
Release:        1%{?dist}
Summary:        Generate realistic-looking sample data in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Faker
Source0:        Data-Faker-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl-generators

%description
Data::Faker generates realistic-looking names, addresses, company names,
dates, telephone numbers, and Internet values for sample data. It includes
the datafaker command-line utility.

%prep
%autosetup -n Data-Faker-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve and run every default upstream test, including the CLI test.
%make_build test

%files
%license README
%doc Changes
%{_bindir}/datafaker
%{perl_vendorlib}/Data/Faker.pm
%{perl_vendorlib}/Data/Faker/*.pm
%{_mandir}/man3/Data::Faker*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10-1
- Package the official CPAN release with its unchanged default test suite.
