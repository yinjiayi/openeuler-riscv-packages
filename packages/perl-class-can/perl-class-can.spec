# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-can
Version:        0.01
Release:        1%{?dist}
Summary:        Inspect Perl classes and inherited methods
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Can
Source0:        https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Class-Can-%{version}.tar.gz
Patch0:         patches/0001-preserve-build-helper-license.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.6
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Class-ISA
BuildRequires:  perl-Devel-Symdump
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Class-ISA
Requires:       perl-Devel-Symdump

%description
Class::Can inspects a class and its inheritance hierarchy, mapping callable
method names to their defining packages, with derived overrides preserved.

%prep
%setup -q -n Class-Can-%{version}
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
%license lib/Class/Can.pm BUILD-HELPER-LICENSE
%{perl_vendorlib}/Class/Can.pm
%{_mandir}/man3/Class::Can.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Preserve the original tests and exact build-helper license declarations.
