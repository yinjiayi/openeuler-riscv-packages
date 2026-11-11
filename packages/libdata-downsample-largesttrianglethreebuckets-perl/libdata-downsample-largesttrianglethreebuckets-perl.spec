# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-DownSample-LargestTriangleThreeBuckets
Version:        1.00
Release:        1%{?dist}
Summary:        Largest-triangle-three-buckets time series downsampling
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Data-DownSample-LargestTriangleThreeBuckets
Source0:        Data-DownSample-LargestTriangleThreeBuckets-%{version}.tar.gz
Patch0:         0001-fix-hash-constructor.patch

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Data::DownSample::LargestTriangleThreeBuckets downsamples time series while
preserving representative points using the largest-triangle-three-buckets
algorithm.

%prep
%autosetup -n Data-DownSample-LargestTriangleThreeBuckets-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Data/DownSample/LargestTriangleThreeBuckets.pm
%{_mandir}/man3/Data::DownSample::LargestTriangleThreeBuckets.3*

%changelog
* Sun Nov 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.00-1
- Package CPAN release with constructor correction and regression tests.
