# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-CSV-Unicode
Version:        0.400
Release:        1%{?dist}
Summary:        Unicode-aware wrapper around Perl Text::CSV
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-CSV-Unicode
Source0:        Text-CSV-Unicode-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Text-CSV
BuildRequires:  perl-generators
Requires:       perl(Text::CSV) >= 1

%description
Text::CSV::Unicode extends Text::CSV with Unicode input handling and
validation while retaining the familiar comma-separated values interface.

%prep
%autosetup -n Text-CSV-Unicode-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all five upstream default t/*.t files, including POD coverage.
./Build test

%files
%license README
%doc Changes examples
%{perl_vendorlib}/Text/CSV/Unicode.pm
%{_mandir}/man3/Text::CSV::Unicode.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.400-1
- Package official CPAN release with all five default test files.
