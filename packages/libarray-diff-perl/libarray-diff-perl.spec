# SPDX-License-Identifier: Apache-2.0
Name:           perl-Array-Diff
Version:        0.09
Release:        1%{?dist}
Summary:        Find the differences between two sorted Perl arrays
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Array-Diff
Source0:        Array-Diff-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Algorithm-Diff
BuildRequires:  perl-Class-Accessor
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Array::Diff compares two pre-sorted arrays and reports their added and
deleted elements through Algorithm::Diff.

%prep
%autosetup -n Array-Diff-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# All six upstream t/*.t files, including four POD and POD-coverage checks.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Array/Diff.pm
%{_mandir}/man3/Array::Diff.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package the official CPAN release and complete upstream test suite.
