# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Formatter
Version:        1.235
Release:        1%{?dist}
Summary:        Build configurable sprintf-like Perl formatters
License:        GPL-2.0-only
URL:            https://metacpan.org/dist/String-Formatter
Source0:        String-Formatter-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Params-Util
BuildRequires:  perl-Sub-Exporter
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Params::Util)
Requires:       perl(Sub::Exporter)

%description
String::Formatter builds sprintf-like formatting routines with configurable
conversion codes and replacement behavior.

%prep
%autosetup -n String-Formatter-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all six default upstream t/*.t suites unchanged.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/String/Formatter.pm
%{perl_vendorlib}/String/Formatter/Cookbook.pm
%{_mandir}/man3/String::Formatter.3*
%{_mandir}/man3/String::Formatter::Cookbook.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.235-1
- Package the official CPAN release and retain all default upstream tests.
