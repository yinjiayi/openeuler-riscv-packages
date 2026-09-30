# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Affixes
Version:        0.09
Release:        1%{?dist}
Summary:        Perl prefix and suffix analysis of text
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Affixes
Source0:        Text-Affixes-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::Affixes extracts frequency counts for prefixes and suffixes in text.

%prep
%autosetup -n Text-Affixes-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all five default upstream tests, including both POD checks.
./Build test

%files
%license LICENSE
%doc README.md Changes
%{perl_vendorlib}/Text/Affixes.pm
%{_mandir}/man3/Text::Affixes.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package official CPAN release with all default tests and functional smoke.
