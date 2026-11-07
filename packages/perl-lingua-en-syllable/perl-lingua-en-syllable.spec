# SPDX-License-Identifier: Apache-2.0
Name:           perl-lingua-en-syllable
Version:        0.31
Release:        1%{?dist}
Summary:        Heuristic English syllable counting for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Lingua-EN-Syllable
Source0:        Lingua-EN-Syllable-0.31.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl-Exporter

%description
Lingua::EN::Syllable estimates syllable counts using English spelling heuristics.
It is intended for approximate text analysis rather than exact pronunciation
lookup. Original upstream behavior and its default test suite are retained.

%prep
%setup -q -n Lingua-EN-Syllable-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install pure_install

%check
make test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Lingua/EN/Syllable.pm
%{_mandir}/man3/Lingua::EN::Syllable.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.31-1
- Package official stable source with complete original default test suite.
