# SPDX-License-Identifier: Apache-2.0
Name:           perl-tree-simple
Version:        1.34
Release:        1%{?dist}
Summary:        Perl tree nodes and visitor traversal
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Tree-Simple
Source0:        https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Tree-Simple-%{version}.tgz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Scalar::Util) >= 1.18
BuildRequires:  perl(constant)
BuildRequires:  perl(Test::Exception) >= 0.15
BuildRequires:  perl(Test::More) >= 1.001002
BuildRequires:  perl(Test::Memory::Cycle) >= 1.02
BuildRequires:  perl(Devel::Cycle) >= 1.07
BuildRequires:  perl(PadWalker)
Requires:       perl
Requires:       perl(Scalar::Util) >= 1.18
Requires:       perl(constant)

%description
Represent and traverse rooted Perl trees with parent and child relationships,
cloning, and customizable visitor callbacks.

%prep
%setup -q -n Tree-Simple-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
perl -e 'use Test::Memory::Cycle 1.02;'
make test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Tree/Simple.pm
%{perl_vendorlib}/Tree/Simple/Visitor.pm
%{_mandir}/man3/Tree::Simple.3pm*
%{_mandir}/man3/Tree::Simple::Visitor.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.34-1
- Package the official fixed release and retain all original cycle tests.
