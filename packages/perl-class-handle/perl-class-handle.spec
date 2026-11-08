# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-handle
Version:        1.07
Release:        1%{?dist}
Summary:        Objects representing Perl classes and their introspection operations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Handle
Source0:        https://cpan.metacpan.org/authors/id/A/AD/ADAMK/Class-Handle-%{version}.tar.gz
Patch0:         0001-preserve-helper-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-PathTools
BuildRequires:  perl-Class-ISA >= 0.31
BuildRequires:  perl-Class-Inspector >= 1.12
BuildRequires:  perl-generators
BuildRequires:  findutils
BuildRequires:  patch
Requires:       perl-Class-ISA >= 0.31
Requires:       perl-Class-Inspector >= 1.12

%description
Class::Handle supplies object handles for class introspection, inheritance and
loading, wrapping UNIVERSAL, Class::ISA and Class::Inspector.

%prep
%setup -q -n Class-Handle-%{version}
%patch -P 0 -p1

%build
perl -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
make test

%files
%license LICENSE BUNDLED-HELPER-NOTICES
%doc README Changes
%{perl_vendorlib}/Class/Handle.pm
%{_mandir}/man3/Class::Handle.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Package fixed release, original tests and bundled helper notices.
