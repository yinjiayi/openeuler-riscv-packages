# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Buffer
Version:        0.06
Release:        1%{?dist}
Summary:        Read and write binary buffers in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Buffer
Source0:        Data-Buffer-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test2-Suite
BuildRequires:  perl-generators

%description
Data::Buffer provides binary buffer read and write methods for primitive
integers, strings, byte ranges and packet-format templates.

%prep
%autosetup -n Data-Buffer-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the sole default upstream test file and all 55 assertions.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Data/Buffer.pm
%{_mandir}/man3/Data::Buffer.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package the official CPAN release with its complete default upstream test.
