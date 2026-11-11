# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Reform
Version:        1.20
Release:        1%{?dist}
Summary:        Format text with configurable Perl field layouts
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Reform
Source0:        Text-Reform-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(POSIX)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::Reform supplies a re-entrant and configurable Perl field-formatting
function, including text wrapping and column formatting.

%prep
%autosetup -n Text-Reform-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all three default upstream t files, including POD syntax.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Text/Reform.pm
%{_mandir}/man3/Text::Reform.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.20-1
- Package official CPAN release with complete default tests and smoke.
