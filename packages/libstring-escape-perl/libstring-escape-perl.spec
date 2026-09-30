# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Escape
Version:        2010.002
Release:        1%{?dist}
Summary:        Perl string quoting, escaping and unescaping helpers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Escape
Source0:        String-Escape-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Pod-Coverage
BuildRequires:  perl-generators
Requires:       perl(Test::More)

%description
String::Escape quotes and unquotes strings, escapes backslashes and
unprintable characters, and offers string-list/hash conversion helpers.

%prep
%autosetup -n String-Escape-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all eight default upstream suites, including the optional POD
# coverage suite; build requirements ensure it executes on the target.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/String/Escape.pm
%{_mandir}/man3/String::Escape.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2010.002-1
- Package official CPAN release with all default upstream suites retained.
