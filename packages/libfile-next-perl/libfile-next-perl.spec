# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Next
Version:        1.18
Release:        1%{?dist}
Summary:        Perl file-finding iterator
License:        Artistic-2.0
URL:            https://metacpan.org/dist/File-Next
Source0:        File-Next-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Temp) >= 0.22
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04

%description
File::Next supplies iterators that walk file and directory trees without
building the entire result list in memory.

%prep
%autosetup -n File-Next-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all default upstream tests, including the FIFO/fork fixture and the
# POD checks enabled by explicit test dependencies.
%make_build test

%files
%doc Changes README.md
%{perl_vendorlib}/File/Next.pm
%{_mandir}/man3/File::Next.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.18-1
- Package the official CPAN release and full default upstream test suite.
