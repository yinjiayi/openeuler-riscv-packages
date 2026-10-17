# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-FormatTable
Version:        1.03
Release:        1%{?dist}
Summary:        Format text tables in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-FormatTable
Source0:        Text-FormatTable-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::FormatTable renders aligned plain-text tables, including wrapped cells.

%prep
%autosetup -n Text-FormatTable-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete
# Upstream MakeMaker puts the example in a generic module namespace;
# package the same source as documentation instead.
rm -f %{buildroot}%{perl_vendorlib}/Text/example.pl

%check
# Retain the complete upstream default test.pl and its five assertions.
%make_build test

%files
%license README
%doc Changes example.pl
%{perl_vendorlib}/Text/FormatTable.pm
%{_mandir}/man3/Text::FormatTable.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package official CPAN release with full default tests and render smoke.
