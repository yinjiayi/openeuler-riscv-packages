# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-HexDump
Version:        0.04
Release:        1%{?dist}
Summary:        Hexadecimal dump formatter for Perl data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-HexDump
Source0:        Data-HexDump-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(parent)
BuildRequires:  perl(Test)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Data::HexDump formats binary data as readable hexadecimal and ASCII dumps,
through a function or object interface.

%prep
%autosetup -n Data-HexDump-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both default upstream tests without exclusions or assertion changes.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Data/HexDump.pm
%{_mandir}/man3/Data::HexDump.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package the official CPAN release with its unchanged default test suite.
