# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Password
Version:        1.12
Release:        1%{?dist}
Summary:        Check Perl password strings against configurable rules
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Password
Source0:        Data-Password-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Pod::Text)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators

%description
Data::Password checks candidate strings against configurable length,
character-class, sequence, and dictionary rules. These checks are not a
substitute for a modern password-strength policy.

%prep
%autosetup -n Data-Password-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all three default upstream tests, including UNIX getpwnam checks.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Data/Password.pm
%{_mandir}/man3/Data::Password.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12-1
- Package the official CPAN release with its unchanged default test suite.
