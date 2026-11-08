# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Munge
Version:        0.111
Release:        1%{?dist}
Summary:        Utility functions for transforming Perl data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Munge
Source0:        Data-Munge-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test2-Suite
BuildRequires:  perl-generators
Requires:       perl(Scalar::Util)

%description
Data::Munge supplies small utility functions for transforming Perl data,
including string trimming, replacement and regular-expression helpers.

%prep
%autosetup -n Data-Munge-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all four default upstream t/ files and the separate upstream POD test.
%make_build test
prove -Iblib/lib xt/pod.t

%files
%license README
%doc Changes
%{perl_vendorlib}/Data/Munge.pm
%{_mandir}/man3/Data::Munge.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.111-1
- Package the official CPAN release with default and POD tests.
