# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Amoeba
Version:        0.05
Release:        1%{?dist}
Summary:        Downhill simplex numerical optimization in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Amoeba
Source0:        Math-Amoeba-%{version}.tar.gz

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
Math::Amoeba minimizes multivariate functions with the downhill simplex
method.

%prep
%autosetup -n Math-Amoeba-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the complete upstream default suite, including both POD tests.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Math/Amoeba.pm
%{_mandir}/man3/Math::Amoeba.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package official CPAN release with complete default tests.
