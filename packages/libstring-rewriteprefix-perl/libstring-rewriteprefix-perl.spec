# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-RewritePrefix
Version:        0.009
Release:        1%{?dist}
Summary:        Rewrite strings using configurable prefixes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-RewritePrefix
Source0:        String-RewritePrefix-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Sub-Exporter
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Sub::Exporter) >= 0.972

%description
String::RewritePrefix rewrites strings by substituting the longest matching
prefix from a configurable mapping. A replacement may also be a callback.

%prep
%autosetup -n String-RewritePrefix-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all three default upstream t/*.t suites unchanged.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/String/RewritePrefix.pm
%{_mandir}/man3/String::RewritePrefix.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.009-1
- Package the official CPAN release and retain all default upstream tests.
