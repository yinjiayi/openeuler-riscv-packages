# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-BitMask
Version:        1.00
Release:        2%{?dist}
Summary:        Named bit-mask construction and explanation for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-BitMask
Source0:        Data-BitMask-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Module::Build) >= 0.42
BuildRequires:  perl(Test)
BuildRequires:  perl-generators

%description
Data::BitMask builds bit masks from named constants and explains mask values
using those constants.

%prep
%autosetup -n Data-BitMask-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the complete upstream default test: 1 file, 137 assertions.
./Build test

%files
%doc README Changes
%{perl_vendorlib}/Data/BitMask.pm
%{_mandir}/man3/Data::BitMask.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.00-2
- Mark the pure-Perl payload noarch and suppress empty ELF debuginfo output.

* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.00-1
- Package the official CPAN release with its full default upstream test.
