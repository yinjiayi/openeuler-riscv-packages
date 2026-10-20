# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Levenshtein-Damerau
Version:        0.41
Release:        1%{?dist}
Summary:        Calculate the Damerau-Levenshtein edit distance in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Levenshtein-Damerau
Source0:        Text-Levenshtein-Damerau-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(List::Util)

%description
Text::Levenshtein::Damerau calculates edit distances between strings,
including adjacent transpositions and Unicode text. This package contains
the upstream pure-Perl implementation and object interface.

%prep
%autosetup -n Text-Levenshtein-Damerau-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all six default upstream t/*.t suites (45 assertions); the two
# upstream xt/*.t POD checks are not registered in the default make test.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/Levenshtein/Damerau.pm
%{perl_vendorlib}/Text/Levenshtein/Damerau/PP.pm
%{_mandir}/man3/Text::Levenshtein::Damerau.3*
%{_mandir}/man3/Text::Levenshtein::Damerau::PP.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.41-1
- Package official CPAN release with all six default test suites.
