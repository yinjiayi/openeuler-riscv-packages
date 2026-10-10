# SPDX-License-Identifier: Apache-2.0
Name:           perl-Set-Infinite
Version:        0.65
Release:        1%{?dist}
Summary:        Sets of finite and infinite intervals for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Set-Infinite
Source0:        Set-Infinite-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::Local)
BuildRequires:  perl-generators
Requires:       perl(Time::Local)

%description
Set::Infinite represents sets of intervals and supports interval
union, intersection, and related operations in pure Perl.

%prep
%autosetup -n Set-Infinite-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every original default t/*.t file without alteration.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Set/Infinite.pm
%{perl_vendorlib}/Set/Infinite/
%{_mandir}/man3/Set::Infinite*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.65-1
- Package the official CPAN release and all original default tests.
