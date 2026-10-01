# SPDX-License-Identifier: Apache-2.0
Name:           perl-Array-Utils
Version:        0.5
Release:        1%{?dist}
Summary:        Pure-Perl array set operations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Array-Utils
Source0:        Array-Utils-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Array::Utils supplies pure-Perl unique, intersection, symmetric
difference, and subtraction operations for lists.

%prep
%autosetup -n Array-Utils-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The complete upstream default suite is the one t/array-utils.t file.
%make_build test

%files
%doc Changes README
%{perl_vendorlib}/Array/Utils.pm
%{_mandir}/man3/Array::Utils.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5-1
- Package the official CPAN release and complete upstream test suite.
