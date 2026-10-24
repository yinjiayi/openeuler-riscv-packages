# SPDX-License-Identifier: Apache-2.0
Name:           perl-Sort-MergeSort
Version:        0.31
Release:        1%{?dist}
Summary:        Merge pre-sorted input streams with Perl iterators
License:        (Artistic-2.0 OR LGPL-2.1-only) AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:            https://metacpan.org/release/Sort-MergeSort
Source0:        Sort-MergeSort-%{version}.tar.gz
Source1:        Artistic-2.0-full-original.md
Source2:        LGPL-2.1-full-original.txt
Source3:        Perl-Artistic-full-original.txt
Source4:        Perl-Copying-full-original.txt
Source5:        Object-Relation-Build-original.txt
Source6:        Object-Relation-Iterator-original.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-NoWarnings
BuildRequires:  perl-podlators
BuildRequires:  perl-generators
BuildRequires:  coreutils
Requires:       perl(Test::NoWarnings)

%description
Sort::MergeSort merges sorted input streams using a supplied comparison
function and filehandles or lightweight iterators. Its Iterator component
provides next, peek, current, position, all and callback traversal methods.

%prep
%autosetup -n Sort-MergeSort-%{version} -p1
# Preserve whole original sources and both substantive default tests.
echo 'e0edaf39c15477ca99a4bef9fb2eaaa920fa919be55af1393ec653648b94dc1e  lib/Sort/MergeSort.pm' | sha256sum -c -
echo 'e26be8ab47e420b6b5770ba18ce9382b3604617a03d2b4195503c79324f29931  lib/Sort/MergeSort/Iterator.pm' | sha256sum -c -
echo '284b4e7ba2dadd11dadac74be3b1d6f7ba1ffa1eca0921eee5bb5c0945d11c71  t/iterator.t' | sha256sum -c -
echo '8e8c14582cd5ecbd56e80be3b97455ba1699a16bb9f76363492fe011b4c62791  t/mergesort.t' | sha256sum -c -
mkdir notices
install -m 0644 lib/Sort/MergeSort.pm notices/Sort-MergeSort-main-original.txt
install -m 0644 lib/Sort/MergeSort/Iterator.pm notices/Sort-MergeSort-Iterator-original.txt
install -m 0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} notices/
# Original historical Build.PL/Iterator bytes are inert attribution documents,
# never executed, loaded as modules, or used as a build dependency.

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both default t/*.t without filters, rewrites or removed assertions.
echo '284b4e7ba2dadd11dadac74be3b1d6f7ba1ffa1eca0921eee5bb5c0945d11c71  t/iterator.t' | sha256sum -c -
echo '8e8c14582cd5ecbd56e80be3b97455ba1699a16bb9f76363492fe011b4c62791  t/mergesort.t' | sha256sum -c -
%make_build test

%files
%license notices/*
%doc README Changes
%{perl_vendorlib}/Sort/MergeSort.pm
%{perl_vendorlib}/Sort/MergeSort/
%{_mandir}/man3/Sort::MergeSort.3*
%{_mandir}/man3/Sort::MergeSort::Iterator.3*

%changelog
* Fri Oct 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.31-1
- Package official CPAN release with both default tests and scoped whole notices.
