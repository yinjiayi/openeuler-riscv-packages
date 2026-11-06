# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-DirList
Version:        0.05
Release:        1%{?dist}
Summary:        Sorted directory listings for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-DirList
Source0:        File-DirList-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::DirList returns directory entries with metadata in a configurable
sort order.

%prep
%autosetup -n File-DirList-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The upstream test prints HOME directory entry names; use an empty private
# HOME so the unchanged test does not expose the builder's files in CI logs.
mkdir -p test-home
HOME="$PWD/test-home" %make_build test

%files
%doc README Changes
%{perl_vendorlib}/File/DirList.pm
%{_mandir}/man3/File::DirList.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package official CPAN release with its complete default test suite.
