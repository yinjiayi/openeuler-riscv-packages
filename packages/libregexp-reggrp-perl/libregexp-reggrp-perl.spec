# SPDX-License-Identifier: Apache-2.0
Name:           libregexp-reggrp-perl
Version:        2.01
Release:        1%{?dist}
Summary:        Group multiple regular-expression substitutions in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Regexp-RegGrp
Source0:        Regexp-RegGrp-2.01.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.10.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.22
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(constant)
BuildRequires:  perl(re)
Requires:       perl >= 5.10.0
Requires:       perl(Carp)
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(constant)
Requires:       perl(re)

%description
Group multiple regular-expression substitutions in Perl

%prep
%autosetup -n Regexp-RegGrp-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Regexp/RegGrp.pm
test -f %{buildroot}%{perl_vendorlib}/Regexp/RegGrp/Data.pm
test -f %{buildroot}%{_mandir}/man3/Regexp::RegGrp.3pm

%check
make test TEST_VERBOSE=1

%files
%license README.md Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Regexp/RegGrp.pm
%dir %{perl_vendorlib}/Regexp/RegGrp
%{perl_vendorlib}/Regexp/RegGrp/Data.pm
%{_mandir}/man3/Regexp::RegGrp.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.01-1
- Package verified source, original tests and a modern-Perl regex smoke test.
