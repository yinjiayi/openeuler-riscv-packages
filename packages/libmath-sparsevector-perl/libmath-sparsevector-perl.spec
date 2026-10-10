# SPDX-License-Identifier: Apache-2.0
Name:           perl-Math-SparseVector
Version:        0.04
Release:        1%{?dist}
Summary:        Sparse vector arithmetic for Perl
License:        GPL-2.0-or-later
URL:            https://metacpan.org/dist/Math-SparseVector
Source0:        Math-SparseVector-%{version}.tar.gz

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
Math::SparseVector provides indexed sparse-vector operations including
addition, normalization and dot products.

%prep
%autosetup -n Math-SparseVector-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete unchanged upstream default test.
%make_build test

%files
%license README
%doc CHANGES
%{perl_vendorlib}/Math/SparseVector.pm
%{perl_vendorlib}/Math/INSTALL.pod
%{_mandir}/man3/Math::SparseVector.3*
%{_mandir}/man3/Math::INSTALL.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package the official CPAN release and complete default test.
