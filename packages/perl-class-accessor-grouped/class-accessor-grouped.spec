# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-accessor-grouped
Version:        0.10014
Release:        1%{?dist}
Summary:        Grouped class and object accessors for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Accessor-Grouped
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Class-Accessor-Grouped-%{version}.tar.gz
Patch0:         patches/0001-preserve-eumm-attribution.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  perl >= 5.6
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Module-Runtime >= 0.012
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Carp
BuildRequires:  perl-Text-ParseWords
BuildRequires:  perl-Test-Simple >= 0.88
BuildRequires:  perl-Test-Exception >= 0.31
BuildRequires:  perl-Class-XSAccessor >= 1.19
BuildRequires:  perl-Sub-Name >= 0.05
BuildRequires:  perl-Devel-Hide
BuildRequires:  perl-Package-Stash
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Module-Runtime >= 0.012
Requires:       perl-Scalar-List-Utils
Requires:       perl-Carp
Requires:       perl-Class-XSAccessor >= 1.19
Requires:       perl-Sub-Name >= 0.05

%description
Class::Accessor::Grouped generates grouped accessors for objects and classes,
including read-only, write-only and inherited accessors. The default upstream
compiler-capable configuration and its supplied XS accessor dependency are kept.

%prep
%setup -q -n Class-Accessor-Grouped-%{version}
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
%license README inc/ExtUtils/HasCompiler.pm BUILD-HELPER-LICENSE
%doc Changes
%{perl_vendorlib}/Class/Accessor/Grouped.pm
%{_mandir}/man3/Class::Accessor::Grouped.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10014-1
- Retain default tests, compiler path and original helper license declarations.
