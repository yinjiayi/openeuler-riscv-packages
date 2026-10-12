# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Binary
Version:        0.01
Release:        1%{?dist}
Summary:        Detect binary versus text strings in Perl
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Data-Binary
Source0:        Data-Binary-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Encode)
BuildRequires:  perl(base)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Data::Binary applies text and binary heuristics to Perl strings rather than
files or file handles.

%prep
%autosetup -n Data-Binary-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve both default upstream test files and all nine assertions.
%make_build test

%files
%license README
%doc INSTALL changes.txt readme.txt
%{perl_vendorlib}/Data/Binary.pm
%{_mandir}/man3/Data::Binary.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package the official CPAN release with its complete default test suite.
