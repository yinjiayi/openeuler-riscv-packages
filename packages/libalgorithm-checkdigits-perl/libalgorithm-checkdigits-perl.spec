# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-CheckDigits
Version:        1.3.6
Release:        1%{?dist}
Summary:        Generate and validate check digits for common identifiers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-CheckDigits
Source0:        Algorithm-CheckDigits-v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl(Probe::Perl)
BuildRequires:  perl(Pod::Usage) >= 1.30
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(version)
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators
Requires:       perl(Pod::Usage) >= 1.30
Requires:       perl(Getopt::Long)
Requires:       perl(version)

%description
Algorithm::CheckDigits implements check-digit algorithms for identifiers,
including IMEI, ISBN, IBAN and UPC. The package includes the checkdigits.pl
command-line tool.

%prep
%autosetup -n Algorithm-CheckDigits-v%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every unmodified default t/ file, including POD coverage and the CLI.
# t/94-version.t self-skips when optional Test::Version is unavailable.
./Build test

%files
%license README
%doc Changes
%{_bindir}/checkdigits.pl
%{perl_vendorlib}/Algorithm/CheckDigits.pm
%{perl_vendorlib}/Algorithm/CheckDigits/
%{_mandir}/man1/checkdigits.pl.1*
%{_mandir}/man3/Algorithm::CheckDigits*.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.6-1
- Package the official CPAN release with all default tests and CLI.
