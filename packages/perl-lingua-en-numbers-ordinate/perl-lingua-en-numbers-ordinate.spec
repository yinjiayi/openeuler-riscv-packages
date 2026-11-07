# SPDX-License-Identifier: Apache-2.0
Name:           perl-lingua-en-numbers-ordinate
Version:        1.05
Release:        1%{?dist}
Summary:        English numeric ordinal suffix conversion for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Lingua-EN-Numbers-Ordinate
Source0:        Lingua-EN-Numbers-Ordinate-1.05.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl-Exporter

%description
Lingua::EN::Numbers::Ordinate provides English ordinal suffixes and numeric
ordinal strings, such as 3rd and 11th. It does not spell numbers as words
or implement the grammar of other languages.

%prep
%setup -q -n Lingua-EN-Numbers-Ordinate-%{version}

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
%{perl_vendorlib}/Lingua/EN/Numbers/Ordinate.pm
%{_mandir}/man3/Lingua::EN::Numbers::Ordinate.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.05-1
- Package the official fixed release and retain the complete default test suite.
