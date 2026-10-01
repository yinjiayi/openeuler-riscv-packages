# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-ASCIITable
Version:        0.22
Release:        1%{?dist}
Summary:        Create formatted ASCII tables in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-ASCIITable
Source0:        Text-ASCIITable-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode)
BuildRequires:  perl(List::Util)
BuildRequires:  perl-generators

%description
Text::ASCIITable renders formatted ASCII tables and includes a text-wrapping
helper module.

%prep
%autosetup -n Text-ASCIITable-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all thirteen upstream default tests and their 111 assertions.
./Build test

%files
%license README
%doc Changes ansi-example.pl
%{perl_vendorlib}/Text/ASCIITable.pm
%{perl_vendorlib}/Text/ASCIITable/Wrap.pm
%{_mandir}/man3/Text::ASCIITable.3*
%{_mandir}/man3/Text::ASCIITable::Wrap.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.22-1
- Package official CPAN release with full upstream tests and table smoke.
