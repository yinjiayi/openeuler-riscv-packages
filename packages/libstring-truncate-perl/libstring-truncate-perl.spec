# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Truncate
Version:        1.100603
Release:        1%{?dist}
Summary:        Truncate and elide Perl strings to a target length
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Truncate
Source0:        String-Truncate-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Sub-Exporter
BuildRequires:  perl-Sub-Install
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Sub::Exporter) >= 0.953
Requires:       perl(Sub::Exporter::Util)
Requires:       perl(Sub::Install) >= 0.03

%description
String::Truncate shortens strings to a target length, either by plain
truncation or with an elision marker. It supports left, right, middle and
both-ends shortening.

%prep
%autosetup -n String-Truncate-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all four unmodified upstream default suites and their 65 checks.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/String/Truncate.pm
%{_mandir}/man3/String::Truncate.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.100603-1
- Package official CPAN release with all four default upstream suites.
