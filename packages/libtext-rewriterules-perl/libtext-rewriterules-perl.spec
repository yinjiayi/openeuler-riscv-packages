# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-RewriteRules
Version:        0.25
Release:        1%{?dist}
Summary:        Rewrite text with regular-expression rules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-RewriteRules
Source0:        Text-RewriteRules-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Filter-Simple
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Filter::Simple) >= 0.78
Requires:       perl(Test::More)

%description
Text::RewriteRules provides regular-expression-based text rewrite rules and
the textrr command for compiling those rules into standalone Perl code.

%prep
%autosetup -n Text-RewriteRules-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve every default upstream test, including its two author-only POD skips.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Text/RewriteRules.pm
%{_bindir}/textrr
%{_mandir}/man1/textrr.1*
%{_mandir}/man3/Text::RewriteRules.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.25-1
- Package official CPAN release with all default upstream tests.
