# SPDX-License-Identifier: Apache-2.0
Name:           perl-class-accessor-lite
Version:        0.08
Release:        1%{?dist}
Summary:        Minimalistic Perl accessor and constructor generation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Accessor-Lite
Source0:        Class-Accessor-Lite-0.08.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators


%description
Class::Accessor::Lite generates read/write, read-only and write-only accessors
and optional constructors for Perl classes without changing their inheritance.

%prep
%autosetup -n Class-Accessor-Lite-%{version}

%build
PERL_AUTOINSTALL=--skipdeps %{__perl} -I. Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Class/Accessor/Lite.pm
%{_mandir}/man3/Class::Accessor::Lite.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package the fixed official release with the complete upstream test suite.
