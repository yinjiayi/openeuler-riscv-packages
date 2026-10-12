# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Tagged
Version:        0.24
Release:        1%{?dist}
Summary:        Mutable Perl strings with tagged character extents
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Tagged
Source0:        String-Tagged-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test2-Suite
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-generators

%description
String::Tagged stores a mutable string together with named values on
character ranges. It supports tagged substring and extent operations.

%prep
%autosetup -n String-Tagged-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# All 22 default upstream t/ files, including t/99pod.t with Test::Pod.
./Build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/String/Tagged.pm
%{perl_vendorlib}/String/Tagged/
%{_mandir}/man3/String::Tagged*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.24-1
- Package official CPAN release with the complete default test suite.
