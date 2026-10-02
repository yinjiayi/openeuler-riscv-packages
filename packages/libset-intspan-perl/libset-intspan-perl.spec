# SPDX-License-Identifier: Apache-2.0
Name:           perl-Set-IntSpan
Version:        1.19
Release:        1%{?dist}
Summary:        Run-length encoded integer sets for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Set-IntSpan
Source0:        Set-IntSpan-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-generators
Requires:       perl

%description
Set::IntSpan stores integer sets as compact runs and supports set
membership, union, intersection, difference, and related operations.

%prep
%autosetup -n Set-IntSpan-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Execute all 20 unchanged original default t/ files.
%make_build test

%files
%license IntSpan.pm
%doc README Changes
%{perl_vendorlib}/Set/IntSpan.pm
%{_mandir}/man3/Set::IntSpan.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.19-1
- Package the official CPAN release and complete original default test suite.
