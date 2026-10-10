# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Capitalize
Version:        1.5
Release:        1%{?dist}
Summary:        Title capitalization utilities for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Capitalize
Source0:        Text-Capitalize-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Env >= 1.00
BuildRequires:  perl(FindBin)
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::Capitalize transforms text into presentable titles and provides
additional case transformation functions.

%prep
%autosetup -n Text-Capitalize-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all nine default upstream t files, including locale cases.
./Build test

%files
%doc README Changes
%{perl_vendorlib}/Text/Capitalize.pm
%{_mandir}/man3/Text::Capitalize.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5-1
- Package official CPAN release with complete default upstream tests.
