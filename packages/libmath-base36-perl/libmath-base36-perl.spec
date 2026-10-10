# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Base36
Version:        0.14
Release:        1%{?dist}
Summary:        Encode and decode base-36 numbers in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Base36
Source0:        Math-Base36-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Math-BigInt
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators

%description
Math::Base36 converts unsigned integers to and from base-36 strings,
including optional zero padding.

%prep
%autosetup -n Math-Base36-%{version} -p1

%build
# Upstream uses inc::Module::Install from this source tree; Perl 5.38 omits
# the current directory from @INC. Keep any existing PERL5LIB for configure.
PERL5LIB="$PWD${PERL5LIB:+:$PERL5LIB}" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all five original t files, including POD and POD coverage.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Math/Base36.pm
%{_mandir}/man3/Math::Base36.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-1
- Package official CPAN release with complete default tests.
