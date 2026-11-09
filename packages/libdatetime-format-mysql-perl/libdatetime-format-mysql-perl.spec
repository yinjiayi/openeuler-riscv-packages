# SPDX-License-Identifier: Apache-2.0
Name:           libdatetime-format-mysql-perl
Version:        0.08
Release:        1%{?dist}
Summary:        Parse and format MySQL dates and times in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/DateTime-Format-MySQL
Source0:        DateTime-Format-MySQL-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Format::Builder) >= 0.60
BuildRequires:  perl(Test::More)
Requires:       perl(DateTime)
Requires:       perl(DateTime::Format::Builder) >= 0.60

%description
DateTime::Format::MySQL parses and formats the date and time strings used
by MySQL, returning or accepting DateTime objects. No server is required.

%prep
%autosetup -n DateTime-Format-MySQL-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build

%install
%{__perl} Build install --destdir=%{buildroot}
find %{buildroot} -type f -name .packlist -delete

%check
# Run all three original upstream default tests without modification.
%{__perl} Build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/DateTime/Format/MySQL.pm
%{_mandir}/man3/DateTime::Format::MySQL.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package the fixed upstream release with the complete default test suite.
