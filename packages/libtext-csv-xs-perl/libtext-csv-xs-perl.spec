# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-CSV_XS
Version:        1.64
Release:        1%{?dist}
Summary:        Fast XS parser and writer for comma-separated values
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-CSV_XS
Source0:        Text-CSV_XS-%{version}.tgz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl-generators

%description
Text::CSV_XS uses an XS extension to parse and compose comma-separated
values, including quoted fields and multiline records.

%prep
%autosetup -n Text-CSV_XS-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all 35 upstream default t/*.t files; no performance claim is made.
%make_build test

%files
%doc README ChangeLog CONTRIBUTING.md SECURITY.md LOVE_LETTER.md examples
%{perl_vendorarch}/Text/CSV_XS.pm
%{perl_vendorarch}/auto/Text/CSV_XS/
%{_mandir}/man3/Text::CSV_XS.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.64-1
- Package official newer CPAN XS release and complete default suite.
