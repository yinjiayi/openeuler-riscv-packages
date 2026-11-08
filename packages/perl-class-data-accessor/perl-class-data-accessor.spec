# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-data-accessor
Version:        0.04004
Release:        1%{?dist}
Summary:        Perl inheritable overridable class and instance data accessors
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Data-Accessor
Source0:        https://cpan.metacpan.org/authors/id/C/CL/CLACO/Class-Data-Accessor-%{version}.tar.gz
Patch0:         0001-preserve-helper-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Carp
BuildRequires:  perl-PathTools
BuildRequires:  perl-podlators
BuildRequires:  perl-generators
Requires:       perl-Carp

%description
Class::Data::Accessor creates inheritable class data accessors with overriding
values for subclasses and hash-based object instances.

%prep
%setup -q -n Class-Data-Accessor-%{version}
%patch -P 0 -p1

%build
PERL_AUTOINSTALL=--skipdeps %{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
make test

%files
%license BUNDLED-HELPER-NOTICES
%doc README Changes
%{perl_vendorlib}/Class/Data/Accessor.pm
%{_mandir}/man3/Class::Data::Accessor.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04004-1
- Preserve original tests and bundled helper notices.
