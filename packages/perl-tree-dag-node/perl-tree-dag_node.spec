# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-tree-dag_node
Version:        1.39
Release:        1%{?dist}
Summary:        Directed acyclic graph nodes for tree structures in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tree-DAG_Node
Source0:        https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Tree-DAG_Node-%{version}.tgz
Patch0:         0001-preserve-forest-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.20.4
BuildRequires:  perl-ExtUtils-MakeMaker >= 7.70
BuildRequires:  perl-File-Slurper >= 0.014
BuildRequires:  perl-Getopt-Long >= 2.57
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Test-Simple >= 1.001002
BuildRequires:  perl-PathTools >= 3.40
BuildRequires:  perl-File-Temp >= 0.19
BuildRequires:  perl-generators
BuildRequires:  findutils
BuildRequires:  patch
Requires:       perl-ExtUtils-MakeMaker >= 7.70
Requires:       perl-File-Slurper >= 0.014
Requires:       perl-Getopt-Long >= 2.57
Requires:       perl-Data-Dumper

%description
Tree::DAG_Node represents tree nodes, relationships, traversal and manipulation,
including textual rendering. It supplies a reusable pure-Perl tree API.

%prep
%setup -q -n Tree-DAG_Node-%{version}
%patch -P 0 -p1

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
%license LICENSE FOREST-NOTICE
%doc README Changes Changelog.ini
%{perl_vendorlib}/Tree/DAG_Node.pm
%{_mandir}/man3/Tree::DAG_Node.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.39-1
- Package fixed source, original tests and adapted Forest renderer notices.
