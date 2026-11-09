# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-sort-versions
Version:        1.62
Release:        1%{?dist}
Summary:        Perl routines for sorting revision-like version strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Sort-Versions
Source0:        https://cpan.metacpan.org/authors/id/N/NE/NEILB/Sort-Versions-%{version}.tar.gz
Patch0:         0001-retain-makemaker-template-license.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  patch
Requires:       perl(Exporter)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Perl routines for sorting revision-like version strings

%prep
%setup -q -n Sort-Versions-%{version}
%patch -P 0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install

%check
make test

%files
%license LICENSE LICENSE.MakeMaker-template
%doc README Changes
%{perl_vendorlib}/Sort/Versions.pm
%{_mandir}/man3/Sort::Versions.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.62-1
- Package fixed release, retain original tests and exact generator notice.
