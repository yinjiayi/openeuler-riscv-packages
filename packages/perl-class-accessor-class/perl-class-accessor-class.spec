# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-accessor-class
Version:        0.504
Release:        1%{?dist}
Summary:        Simple shared class variable accessors in Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0
URL:            https://metacpan.org/dist/Class-Accessor-Class
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Class-Accessor-Class-%{version}.tar.gz
Patch0:         0001-preserve-helper-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.12
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.78
BuildRequires:  perl-Class-Accessor >= 0.16
BuildRequires:  perl-Test-Simple >= 0.96
BuildRequires:  perl-PathTools
BuildRequires:  perl-parent
BuildRequires:  perl-generators
BuildRequires:  findutils
BuildRequires:  patch
Requires:       perl-Class-Accessor >= 0.16
Requires:       perl-parent

%description
Class::Accessor::Class creates accessors for class data shared between classes
and instances, while retaining ordinary Class::Accessor functionality.

%prep
%setup -q -n Class-Accessor-Class-%{version}
%patch -P 0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
make test

%files
%license LICENSE GENERATED-HELPER-NOTICES GENERATED-HELPER-APACHE-LICENSE
%doc README Changes
%{perl_vendorlib}/Class/Accessor/Class.pm
%{_mandir}/man3/Class::Accessor::Class.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.504-1
- Preserve original default tests and complete generated helper notices.
