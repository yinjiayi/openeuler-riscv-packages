# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-lingua-en-namecase
Version:        1.21
Release:        1%{?dist}
Summary:        Heuristic capitalization of personal names for Perl
License:        Artistic-2.0 AND Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Lingua-EN-NameCase
Source0:        Lingua-EN-NameCase-%{version}.tar.gz
Patch0:         0001-retain-nameparse-license-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Most
BuildRequires:  perl-generators
Requires:       perl-Exporter
Requires:       perl-Carp

%description
Lingua::EN::NameCase heuristically normalizes capitalization of personal
names, including several Western prefixes and Roman numerals. It does
not validate identities or establish a person's preferred name spelling.

%prep
%setup -q -n Lingua-EN-NameCase-%{version}
%patch -P 0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license LICENSE COPYING.NameParse COPYING.Artistic1 COPYING.Artistic2
%doc README README.md Changes
%{perl_vendorlib}/Lingua/EN/NameCase.pm
%{_mandir}/man3/Lingua::EN::NameCase.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.21-1
- Package the complete upstream default tests and restore borrowed-code notices.
