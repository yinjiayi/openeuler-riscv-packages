# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Find-Wanted
Version:        1.00
Release:        1%{?dist}
Summary:        Direct wrapper around Perl File::Find
License:        Artistic-2.0
URL:            https://metacpan.org/dist/File-Find-Wanted
Source0:        File-Find-Wanted-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators

%description
File::Find::Wanted accepts a predicate and returns matching paths found
under one or more directory roots.

%prep
%autosetup -n File-Find-Wanted-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all four default upstream tests, including POD and coverage checks.
%make_build test

%files
%doc README.md Changes
%{perl_vendorlib}/File/Find/Wanted.pm
%{_mandir}/man3/File::Find::Wanted.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.00-1
- Package official CPAN release with all default upstream tests.
