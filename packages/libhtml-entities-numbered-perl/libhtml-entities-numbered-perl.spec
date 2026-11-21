# SPDX-License-Identifier: Apache-2.0
Name:           libhtml-entities-numbered-perl
Version:        0.04
Release:        1%{?dist}
Summary:        Convert between named and numeric HTML character references
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/HTML-Entities-Numbered
Source0:        HTML-Entities-Numbered-0.04.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(base)
BuildRequires:  perl(vars)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::More) >= 0.32
Requires:       perl
Requires:       perl(strict)
Requires:       perl(base)
Requires:       perl(vars)
Requires:       perl(Exporter)

%description
Convert between named and numeric HTML character references

%prep
%autosetup -n HTML-Entities-Numbered-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .
cat <<'DONOR_NOTICE' > HTML-Entities-NOTICE
The 253 numeric mappings in the bundled Table.pm and the corresponding
252-row test fixture match the HTML::Entities table in HTML-Parser 3.36.
Copyright 1995-2003 Gisle Aas. All rights reserved.
Redistributable under the same terms as Perl itself; see the accompanying
Artistic-1.0-Perl.txt and GPL-1.0.txt.
Source: https://cpan.metacpan.org/authors/id/G/GA/GAAS/HTML-Parser-3.36.tar.gz
DONOR_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/HTML/Entities/Numbered.pm
test -f %{buildroot}%{perl_vendorlib}/HTML/Entities/Numbered/Table.pm
test -f %{buildroot}%{_mandir}/man3/HTML::Entities::Numbered.3pm
test -f %{buildroot}%{_mandir}/man3/HTML::Entities::Numbered::Table.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt HTML-Entities-NOTICE
%doc Changes
%{perl_vendorlib}/HTML/Entities/Numbered.pm
%{perl_vendorlib}/HTML/Entities/Numbered/Table.pm
%{_mandir}/man3/HTML::Entities::Numbered.3pm*
%{_mandir}/man3/HTML::Entities::Numbered::Table.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package the original module, entity data, tests, and upstream notices.
