# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Undiacritic
Version:        0.07
Release:        1%{?dist}
Summary:        Remove diacritics from Unicode strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Undiacritic
Source0:        Text-Undiacritic-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Unicode::Normalize)
BuildRequires:  perl(charnames)
BuildRequires:  perl-Module-Build-Tiny
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Unicode::Normalize)

%description
Text::Undiacritic removes diacritics and maps selected characters without
Unicode decomposition to their base forms.

%prep
%autosetup -n Text-Undiacritic-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all three default tests and activate their release POD syntax test.
RELEASE_TESTING=1 ./Build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/Undiacritic.pm
%{_mandir}/man3/Text::Undiacritic.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package official CPAN release with all default tests and installed smoke.
