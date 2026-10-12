# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-CheckTree
Version:        4.42
Release:        1%{?dist}
Summary:        Perl module for checking file tests across directory trees
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-CheckTree
Source0:        File-CheckTree-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)

%description
File::CheckTree provides the validate function for checking file tests
through a directory tree and reporting or raising failures.

%prep
%autosetup -n File-CheckTree-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the complete upstream default suite, including the two release-only
# tests that self-skip unless RELEASE_TESTING is explicitly enabled upstream.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/File/CheckTree.pm
%{_mandir}/man3/File::CheckTree.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.42-1
- Package the official stable CPAN release and upstream default test suite.
