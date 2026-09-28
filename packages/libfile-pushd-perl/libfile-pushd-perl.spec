# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-pushd
Version:        1.016
Release:        1%{?dist}
Summary:        Perl module for scoped temporary directory changes
License:        Apache-2.0
URL:            https://metacpan.org/dist/File-pushd
Source0:        File-pushd-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.96

%description
File::pushd changes the working directory for the lifetime of a scoped
object, restoring the original directory when that object is destroyed.
It can also create and manage temporary directories.

%prep
%autosetup -n File-pushd-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all four default upstream test files, including directory, tempdir,
# exception, void-context, and fork-owner behavior where supported.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/File/pushd.pm
%{_mandir}/man3/File::pushd.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.016-1
- Package the official stable CPAN release and full default upstream tests.
