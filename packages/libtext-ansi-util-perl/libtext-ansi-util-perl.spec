# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-ANSI-Util
Version:        0.234
Release:        1%{?dist}
Summary:        Utilities for text containing ANSI escape codes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-ANSI-Util
Source0:        Text-ANSI-Util-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Data-Dump
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(List::Util) >= 1.54

%description
Text::ANSI::Util provides text length, wrapping, stripping, truncation and
other operations that account for ANSI terminal escape codes.

%prep
%autosetup -n Text-ANSI-Util-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run unmodified upstream defaults: operational 00-compile/01-latin; the
# three author-only files explicitly SKIP without AUTHOR_TESTING.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Text/ANSI/BaseUtil.pm
%{perl_vendorlib}/Text/ANSI/Util.pm
%{_mandir}/man3/Text::ANSI::BaseUtil.3*
%{_mandir}/man3/Text::ANSI::Util.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.234-1
- Package official CPAN release with unmodified default operational tests.
