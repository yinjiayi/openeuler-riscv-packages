# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Section-Simple
Version:        0.07
Release:        2%{?dist}
Summary:        Read named sections from Perl DATA handles
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Artistic-2.0
URL:            https://metacpan.org/dist/Data-Section-Simple
Source0:        Data-Section-Simple-%{version}.tar.gz
Source1:        LICENSE.Mojo
Patch0:         0001-document-mojo-parser-provenance.patch

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Requires
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Data::Section::Simple extracts named text sections from a Perl DATA handle,
using functional or object-oriented interfaces without external runtime modules.

%prep
%autosetup -n Data-Section-Simple-%{version} -p1
cp -p %{SOURCE1} LICENSE.Mojo

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install pure_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all five default files and activate upstream release POD validation.
RELEASE_TESTING=1 %make_build test

%files
%license LICENSE LICENSE.Mojo MOJO-PROVENANCE
%doc README Changes
%{perl_vendorlib}/Data/Section/Simple.pm
%{_mandir}/man3/Data::Section::Simple.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-2
- Preserve historical Mojo Artistic-2.0 terms and derivative provenance.
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package official source with full functional and release POD tests.
