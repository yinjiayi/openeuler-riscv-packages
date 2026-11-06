# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-CamelCase
Version:        0.04
Release:        1%{?dist}
Summary:        Convert between camel case and underscore-separated names
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-CamelCase
Source0:        String-CamelCase-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators

%description
String::CamelCase converts names between camel case and underscore-separated
forms and splits names into words.

%prep
%autosetup -n String-CamelCase-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all six default files. Explicit POD dependencies prevent the
# upstream conditional POD/coverage files from silently skipping in CI.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/String/CamelCase.pm
%{_mandir}/man3/String::CamelCase.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package official CPAN release with all six default upstream test files.
