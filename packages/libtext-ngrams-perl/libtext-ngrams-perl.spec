# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Ngrams
Version:        2.007
Release:        1%{?dist}
Summary:        Analyze character and word n-grams in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Ngrams
Source0:        Text-Ngrams-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Getopt::Long)

%description
Text::Ngrams analyzes character and word n-grams from text. The package
includes the ngrams.pl command for command-line analysis.

%prep
%autosetup -n Text-Ngrams-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all fifteen default upstream tests and checked-in expected outputs.
%make_build test

%files
%license README
%doc Changes
%{_bindir}/ngrams.pl
%{perl_vendorlib}/Text/Ngrams.pm
%{perl_vendorlib}/Text/ngrams.pl
%{_mandir}/man1/ngrams.pl.1*
%{_mandir}/man3/Text::Ngrams.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.007-1
- Package official CPAN release with complete default tests and CLI smoke.
