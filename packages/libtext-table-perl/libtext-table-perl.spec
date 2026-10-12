# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Table
Version:        1.135
Release:        1%{?dist}
Summary:        Organize tabular data for text display in Perl
License:        ISC
URL:            https://metacpan.org/dist/Text-Table
Source0:        Text-Table-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Text-Aligner
BuildRequires:  perl-generators
Requires:       perl(Text::Aligner)

%description
Text::Table formats rows and columns into readable text tables with
configurable headings, rules and alignment.

%prep
%autosetup -n Text-Table-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all seven default upstream t/ suites; xt/ suites are for authors.
%make_build test

%files
%license LICENSE
%doc README Changes examples
%{perl_vendorlib}/Text/Table.pm
%{_mandir}/man3/Text::Table.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.135-1
- Package official CPAN release with all default table-formatting tests.
