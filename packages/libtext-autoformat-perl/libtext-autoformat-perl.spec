# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Autoformat
Version:        1.75
Release:        1%{?dist}
Summary:        Automatically wrap and reformat text in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Autoformat
Source0:        Text-Autoformat-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(Text::Reform)
BuildRequires:  perl(Text::Tabs)
Requires:       perl(Text::Reform)

%description
Text::Autoformat provides automatic text wrapping and reformatting,
including configurable paragraph and list handling.

%prep
%autosetup -n Text-Autoformat-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the complete upstream default t/*.t suite.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/Autoformat.pm
%{perl_vendorlib}/Text/Autoformat/
%{_mandir}/man3/Text::Autoformat*.3*

%changelog
* Sat Oct 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.75-1
- Package official CPAN release with its default tests.
