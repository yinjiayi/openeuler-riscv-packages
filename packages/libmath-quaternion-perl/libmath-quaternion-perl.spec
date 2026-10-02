# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Quaternion
Version:        0.07
Release:        1%{?dist}
Summary:        Quaternion arithmetic and rotations in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Quaternion
Source0:        Math-Quaternion-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl-Carp

%description
Math::Quaternion represents quaternions and provides arithmetic, rotation
and interpolation operations in Perl.

%prep
%autosetup -n Math-Quaternion-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve both original test files and all 108 assertions.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Math/Quaternion.pm
%{_mandir}/man3/Math::Quaternion.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package official CPAN release with complete default tests.
