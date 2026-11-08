# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Bezier
Version:        0.01
Release:        1%{?dist}
Summary:        Solve and sample Bezier curves in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Bezier
Source0:        Math-Bezier-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Math::Bezier evaluates and samples two-dimensional Bezier curves from
control points.

%prep
%autosetup -n Math-Bezier-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# MakeMaker runs the original test.pl (27 assertions) as its default test.
%make_build test

%files
%license Bezier.pm
%doc README Changes
%{perl_vendorlib}/Math/Bezier.pm
%{_mandir}/man3/Math::Bezier.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package official CPAN release with its complete default test target.
