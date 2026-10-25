# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Combinatorics
Version:        0.27
Release:        1%{?dist}
Summary:        Efficient combinatorial sequence generators for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-Combinatorics
Source0:        Algorithm-Combinatorics-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Pod-Coverage
BuildRequires:  perl-generators

%description
Algorithm::Combinatorics provides C-backed iterators and list-context
generators for permutations, combinations, partitions, and related sequences.

%prep
%autosetup -n Algorithm-Combinatorics-%{version} -p1

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
%{perl_vendorarch}/Algorithm/Combinatorics.pm
%{perl_vendorarch}/auto/Algorithm/Combinatorics/
%{_mandir}/man3/Algorithm::Combinatorics.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.27-1
- Package the official CPAN XS release with its complete default test suite.
