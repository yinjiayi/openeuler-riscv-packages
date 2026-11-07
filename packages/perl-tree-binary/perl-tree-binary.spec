# SPDX-License-Identifier: Apache-2.0
Name:           perl-tree-binary
Version:        1.09
Release:        1%{?dist}
Summary:        Object-oriented binary trees and traversals in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tree-Binary
Source0:        https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Tree-Binary-%{version}.tgz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.6
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-constant
BuildRequires:  perl-Test-Simple >= 1.001014
BuildRequires:  perl-Test-Exception >= 0.15
BuildRequires:  perl-Test-Pod >= 1.48
BuildRequires:  perl-Test-Pod-Coverage >= 1.10
BuildRequires:  perl-Test-Memory-Cycle
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Scalar-List-Utils
Requires:       perl-constant

%description
Tree::Binary implements binary trees, binary search trees, nodes and visitor
objects for breadth-first and depth-first traversal orders.

%prep
%setup -q -n Tree-Binary-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
make test

%files
%license LICENSE README
%doc Changes
%{perl_vendorlib}/Tree/Binary.pm
%{perl_vendorlib}/Tree/Binary/
%{_mandir}/man3/Tree::Binary*.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.09-1
- Package fixed original source and complete default tests.
