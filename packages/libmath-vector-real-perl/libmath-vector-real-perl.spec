# SPDX-License-Identifier: Apache-2.0
Name:           perl-Math-Vector-Real
Version:        0.18
Release:        1%{?dist}
Summary:        Real vector arithmetic for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Vector-Real
Source0:        Math-Vector-Real-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl

%description
Math::Vector::Real provides arithmetic for real vectors of any dimension,
including norms, dot and cross products, and rotations.

%prep
%autosetup -n Math-Vector-Real-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The unchanged upstream default test explicitly exercises pure Perl.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Math/Vector/Real.pm
%{perl_vendorlib}/Math/Vector/Real/Test.pm
%{_mandir}/man3/Math::Vector::Real.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18-1
- Package official CPAN release with the complete default test.
