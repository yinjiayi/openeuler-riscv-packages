# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Expand
Version:        0.04
Release:        1%{?dist}
Summary:        Expand variables in Perl strings and self-referential maps
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Expand
Source0:        String-Expand-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-generators

%description
String::Expand expands variable references in individual strings or in maps
whose values can refer to one another. It detects missing variables and
reference loops.

%prep
%autosetup -n String-Expand-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all four default upstream suites. Test::Pod is required so 99pod.t
# runs rather than reporting an optional dependency SKIP.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/String/Expand.pm
%{_mandir}/man3/String::Expand.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package official CPAN release with all four default upstream suites.
