# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Metaphone
Version:        20160805
Release:        1%{?dist}
Summary:        Encode English words with the Metaphone phonetic algorithm
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Metaphone
Source0:        Text-Metaphone-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Test::More) >= 0.47

%description
Text::Metaphone provides a compiled Perl XS implementation of the Metaphone
algorithm for approximate English word pronunciation matching.

%prep
%autosetup -n Text-Metaphone-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the complete original default XS test suite.
%make_build test

%files
%doc README Changes INSTALL
%{perl_vendorarch}/Text/Metaphone.pm
%{perl_vendorarch}/auto/Text/Metaphone/Metaphone.so
%{_mandir}/man3/Text::Metaphone.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20160805-1
- Package official CPAN XS release with all default upstream tests.
