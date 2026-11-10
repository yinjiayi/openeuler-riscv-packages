# SPDX-License-Identifier: Apache-2.0
Name:           perl-safe-isa
Version:        1.000010
Release:        1%{?dist}
Summary:        Call Perl object introspection methods safely
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Safe-Isa
Source0:        Safe-Isa-1.000010.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.006
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl >= 5.006
Requires:       perl(Exporter) >= 5.57
Requires:       perl(Scalar::Util)

%description
Safe::Isa supplies callable Perl helpers that invoke isa, can, does
and DOES only on objects, preserving scalar and list context.

%prep
%autosetup -n Safe-Isa-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
# The released META.yml prevents the upstream maintainer-only Distar path.
test -s META.yml
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Safe/Isa.pm
%{_mandir}/man3/Safe::Isa.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.000010-1
- Package the fixed upstream release and preserve its original default tests.
