# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Util
Version:        1.36
Release:        1%{?dist}
Summary:        String processing utility functions for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Util
Source0:        String-Util-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Util provides trimming, whitespace normalization, substring,
escaping, and other small string-processing functions for Perl programs.

%prep
%autosetup -n String-Util-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep both default upstream test files, including substring regressions.
%make_build test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/String/Util.pm
%{_mandir}/man3/String::Util.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.36-1
- Package official current CPAN release and retain all default upstream tests.
