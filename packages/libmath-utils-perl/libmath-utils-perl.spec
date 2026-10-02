# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Utils
Version:        1.14
Release:        1%{?dist}
Summary:        Additional mathematical utility functions for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Utils
Source0:        Math-Utils-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-generators
Requires:       perl >= 5.10.1

%description
Math::Utils provides numerical comparison, summation, number-theory,
scaling and polynomial functions for Perl.

%prep
%autosetup -n Math-Utils-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all 22 original t/*.t files, including the POD test and the
# upstream release-author manifest test's explicit skip.
./Build test

%files
%license LICENSE
%doc Changes README.md CONTRIBUTING.md eg
%{perl_vendorlib}/Math/Utils.pm
%{_mandir}/man3/Math::Utils.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-1
- Package official CPAN release with complete default tests.
