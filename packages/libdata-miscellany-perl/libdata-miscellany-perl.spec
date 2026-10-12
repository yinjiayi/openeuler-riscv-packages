# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Miscellany
Version:        1.100850
Release:        1%{?dist}
Summary:        Collection of miscellaneous Perl utility subroutines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Miscellany
Source0:        Data-Miscellany-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(English)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Data::Miscellany offers small Perl routines for set-like list insertion,
deep comparisons, mapping and string cleanup.

%prep
%autosetup -n Data-Miscellany-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every default upstream test; upstream author/release-only files self-skip.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Data/Miscellany.pm
%{_mandir}/man3/Data::Miscellany.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.100850-1
- Package the official CPAN release with its unchanged default test suite.
