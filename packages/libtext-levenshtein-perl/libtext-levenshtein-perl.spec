# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Levenshtein
Version:        0.15
Release:        1%{?dist}
Summary:        Calculate the Levenshtein edit distance between strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Levenshtein
Source0:        Text-Levenshtein-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Unicode-Collate
BuildRequires:  perl-generators
Requires:       perl(Unicode::Collate) >= 1.04

%description
Text::Levenshtein calculates the edit distance between two strings, including
Unicode text.

%prep
%autosetup -n Text-Levenshtein-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all nine default upstream suites, including Unicode cases.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/Levenshtein.pm
%{_mandir}/man3/Text::Levenshtein.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15-1
- Package official CPAN release with all default Unicode tests.
