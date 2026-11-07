# SPDX-License-Identifier: Apache-2.0
Name:           perl-lingua-en-inflect-number
Version:        1.12
Release:        1%{?dist}
Summary:        Singular and plural noun conversion for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Lingua-EN-Inflect-Number
Source0:        Lingua-EN-Inflect-Number-1.12.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl-Lingua-EN-Inflect
Requires:       perl-Exporter
Requires:       perl-Lingua-EN-Inflect

%description
Lingua::EN::Inflect::Number adds number, to_S and to_PL functions to
Lingua::EN::Inflect. It identifies singular, plural and ambiguous noun
forms and converts them to the requested number. Upstream warns that
this relies on undocumented dependency behavior and is reliable only
for nouns; future dependency changes may require rework.

%prep
%autosetup -n Lingua-EN-Inflect-Number-%{version}

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
%{perl_vendorlib}/Lingua/EN/Inflect/Number.pm
%{_mandir}/man3/Lingua::EN::Inflect::Number.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12-1
- Package the fixed upstream release with its complete original default tests.
