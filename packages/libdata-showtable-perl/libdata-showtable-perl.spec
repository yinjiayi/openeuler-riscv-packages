# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-ShowTable
Version:        4.6
Release:        1%{?dist}
Summary:        Format columnar data as text or HTML tables
License:        GPL-2.0-or-later
URL:            https://metacpan.org/dist/Data-ShowTable
Source0:        Data-ShowTable-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl-generators

%description
Data::ShowTable renders rows of columnar data as simple, boxed, list-style,
or HTML tables. The distribution also installs the showtable command-line
filter.

%prep
%autosetup -n Data-ShowTable-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all 22 upstream test files and their 161 bundled reference outputs.
%make_build test

%files
%license Copyright GNU-LICENSE
%doc Changes README
%{perl_vendorlib}/Data/ShowTable.pm
%{_bindir}/showtable
%{_mandir}/man1/showtable.1*
%{_mandir}/man3/Data::ShowTable.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.6-1
- Package the official CPAN release with its unchanged default test suite.
