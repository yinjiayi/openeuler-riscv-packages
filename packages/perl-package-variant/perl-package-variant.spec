# SPDX-License-Identifier: Apache-2.0
Name:           perl-package-variant
Version:        1.003002
Release:        1%{?dist}
Summary:        Parameterize Perl packages with runtime variants
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Package-Variant
Source0:        https://cpan.metacpan.org/authors/id/M/MS/MSTROUT/Package-Variant-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Import::Into) >= 1.000000
BuildRequires:  perl(Module::Runtime) >= 0.013
BuildRequires:  perl(strictures) >= 2.000000
BuildRequires:  perl(Moo)
BuildRequires:  perl(Moo::Role)
BuildRequires:  perl(Sub::Name)
Requires:       perl
Requires:       perl(Import::Into) >= 1.000000
Requires:       perl(Module::Runtime) >= 0.013
Requires:       perl(strictures) >= 2.000000
Requires:       perl(Carp)
Recommends:     perl(Sub::Name)

%description
Create named or anonymous Perl package variants at runtime, with optional
parameterized role use.

%prep
%setup -q -n Package-Variant-%{version}

%build
test -s META.yml
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Package/Variant.pm
%{_mandir}/man3/Package::Variant.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.003002-1
- Package the fixed release and retain its full default suite and optional Moo tests.
