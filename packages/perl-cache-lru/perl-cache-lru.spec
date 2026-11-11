# SPDX-License-Identifier: Apache-2.0
Name:           perl-Cache-LRU
Version:        0.04
Release:        1%{?dist}
Summary:        Simple in-process least-recently-used cache for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Cache-LRU
Source0:        Cache-LRU-0.04.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Requires
BuildRequires:  perl-generators
BuildRequires:  perl(Pod::Text)
BuildArch:      noarch
Requires:       perl(Scalar::Util)

%description
Simple in-process least-recently-used cache for Perl

%prep
%autosetup -p1 -n Cache-LRU-%{version}

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Cache/LRU.pm
%{_mandir}/man3/Cache::LRU.3*

%changelog
* Thu Oct 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package Cache::LRU with its complete upstream test suite.
