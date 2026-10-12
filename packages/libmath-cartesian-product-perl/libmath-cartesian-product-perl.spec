# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Cartesian-Product
Version:        1.009
Release:        1%{?dist}
Summary:        Generate Cartesian products of Perl lists
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Cartesian-Product
Source0:        Math-Cartesian-Product-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Math::Cartesian::Product generates Cartesian products from zero or more Perl
lists and applies a caller-provided selection callback.

%prep
%autosetup -n Math-Cartesian-Product-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve upstream's complete unmodified one-file, 88-assertion suite.
./Build test

%files
%license README
%doc CHANGES
%{perl_vendorlib}/Math/Cartesian/Product.pm
%{_mandir}/man3/Math::Cartesian::Product.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.009-1
- Package official CPAN release with complete default tests.
