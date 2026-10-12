# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Rmap
Version:        0.65
Release:        1%{?dist}
Summary:        Recursively map Perl data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Rmap
Source0:        Data-Rmap-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Data::Rmap recursively traverses Perl hashes, arrays, scalar references
and globs, applying a caller-supplied block to selected elements.

%prep
%autosetup -n Data-Rmap-%{version} -p1

%build
# Use the upstream-generated Makefile.PL, avoiding Build.PL's author-only action.
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the sole default upstream test file and all its assertions.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/Data/Rmap.pm
%{_mandir}/man3/Data::Rmap.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.65-1
- Package the official CPAN release with its complete default test suite.
