# SPDX-License-Identifier: Apache-2.0
Name:           perl-Call-Context
Version:        0.05
Release:        1%{?dist}
Summary:        Sanity-check Perl calling context
License:        MIT
URL:            https://metacpan.org/dist/Call-Context
Source0:        Call-Context-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Call::Context validates that a calling function is invoked in list context,
or outside scalar context, and throws descriptive exceptions on misuse.

%prep
%autosetup -n Call-Context-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install pure_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the full three-file upstream default test suite.
%make_build test

%files
%license LICENSE
%doc README.md Changes Todo
%{perl_vendorlib}/Call/Context.pm
%{_mandir}/man3/Call::Context.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package official Call::Context release and its full default test suite.
