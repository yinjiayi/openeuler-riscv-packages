# SPDX-License-Identifier: Apache-2.0
Name:           perl-tree-multinode
Version:        2.02
Release:        1%{?dist}
Summary:        Multi-node trees and independent navigation handles in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tree-MultiNode
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/Tree-MultiNode-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.8
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Scalar-List-Utils

%description
Tree::MultiNode models hierarchical data with multi-node trees, internal node
objects and independent handles for navigation and manipulation.

%prep
%setup -q -n Tree-MultiNode-%{version}

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
%license LICENSE
%doc README.md Changes
%{perl_vendorlib}/Tree/MultiNode.pm
%{perl_vendorlib}/Tree/MultiNode/
%{_mandir}/man3/Tree::MultiNode*.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.02-1
- Package fixed release with its complete original default tests.
