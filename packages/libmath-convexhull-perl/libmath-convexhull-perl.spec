# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-ConvexHull
Version:        1.04
Release:        1%{?dist}
Summary:        Calculate two-dimensional convex hulls in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-ConvexHull
Source0:        Math-ConvexHull-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators

%description
Math::ConvexHull calculates the convex hull of two-dimensional points
using Graham's scan.

%prep
%autosetup -n Math-ConvexHull-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all four original t/*.t files, including POD and POD coverage.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Math/ConvexHull.pm
%{_mandir}/man3/Math::ConvexHull.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Package official CPAN release with all default tests.
