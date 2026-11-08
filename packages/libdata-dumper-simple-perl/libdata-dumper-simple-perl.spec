# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Dumper-Simple
Version:        0.11
Release:        1%{?dist}
Summary:        Source-filtered named variable dumps for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Dumper-Simple
Source0:        Data-Dumper-Simple-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Filter::Simple) >= 0.77
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Filter::Simple) >= 0.77
Requires:       perl(Test::More)

%description
Data::Dumper::Simple is a Perl source filter that names variables in
Data::Dumper output without requiring manual name lists.

%prep
%autosetup -n Data-Dumper-Simple-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all six default upstream tests, including POD syntax and coverage.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/Data/Dumper/Simple.pm
%{_mandir}/man3/Data::Dumper::Simple.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package the official CPAN release with all six default upstream tests.
