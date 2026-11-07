# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-BaseCnv
Version:        1.14
Release:        1%{?dist}
Summary:        Convert values between numeric bases in Perl
License:        GPL-3.0-or-later
URL:            https://metacpan.org/dist/Math-BaseCnv
Source0:        Math-BaseCnv-%{version}.tgz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Math-BigInt
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators

%description
Math::BaseCnv provides conversions among numeric bases and includes
the upstream cnv command-line interface.

%prep
%autosetup -n Math-BaseCnv-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all three original t files, including POD and POD coverage.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Math/BaseCnv.pm
%{_bindir}/cnv
%{_mandir}/man3/Math::BaseCnv.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-1
- Package official CPAN release with default tests and command-line tool.
