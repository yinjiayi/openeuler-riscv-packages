# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Permute
Version:        0.17
Release:        1%{?dist}
Summary:        Generate list permutations with Perl XS
License:        LicenseRef-Algorithm-Permute-CDROM-Commercial-Restriction
URL:            https://metacpan.org/dist/Algorithm-Permute
Source0:        Algorithm-Permute-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-LeakTrace
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Algorithm::Permute implements permutation iterators and a callback interface
using Perl XS. It supports choosing a subset length and resetting iterators.
This draft is held for unresolved file-specific commercial-media restrictions;
the LicenseRef records that notice and does not establish redistribution approval.

%prep
%autosetup -n Algorithm-Permute-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install pure_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all default files and activate upstream POD and memory-leak checks.
AUTHOR_TESTING=1 MEMORY_TEST=1 %make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorarch}/Algorithm/Permute.pm
%{perl_vendorarch}/auto/Algorithm/Permute/
%{_mandir}/man3/Algorithm::Permute.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Package official XS release with complete functional, POD and leak tests.
- Record unresolved file-specific commercial-media restriction; hold publication.
