# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-DHCPLeases
Version:        1.0
Release:        1%{?dist}
Summary:        Parse ISC DHCP server lease files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-DHCPLeases
Source0:        Text-DHCPLeases-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Class::Struct) >= 0.63

%description
Text::DHCPLeases parses ISC DHCP server lease files and provides object and
iterator access to lease records.

%prep
%autosetup -n Text-DHCPLeases-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}

%check
# Retain both default upstream fixture-based test files.
./Build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Text/DHCPLeases.pm
%{perl_vendorlib}/Text/DHCPLeases/Object.pm
%{perl_vendorlib}/Text/DHCPLeases/Object/Iterator.pm
%{_mandir}/man3/Text::DHCPLeases.3*
%{_mandir}/man3/Text::DHCPLeases::Object.3*
%{_mandir}/man3/Text::DHCPLeases::Object::Iterator.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0-1
- Package official CPAN release with both default fixture-based test suites.
