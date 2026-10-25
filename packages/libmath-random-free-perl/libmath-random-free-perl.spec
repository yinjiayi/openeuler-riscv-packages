# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Random-Free
Version:        0.2.0
Release:        1%{?dist}
Summary:        Non-cryptographic random distribution functions in Perl
License:        BSD-3-Clause
URL:            https://metacpan.org/dist/Math-Random-Free
Source0:        Math-Random-Free-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Digest-SHA
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl-Digest-SHA
Requires:       perl-Scalar-List-Utils

%description
Math::Random::Free provides non-cryptographic random distributions,
permutations and seed control as a partial Math::Random replacement.

%prep
%autosetup -n Math-Random-Free-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the complete original default test file and its four assertions.
%make_build test

%files
%license LICENSE README
%doc Changes
%{perl_vendorlib}/Math/Random/Free.pm
%{_mandir}/man3/Math::Random::Free.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Package official CPAN release with complete default tests.
