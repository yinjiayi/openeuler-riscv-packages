# SPDX-License-Identifier: Apache-2.0
Name:           perl-Number-Bytes-Human
Version:        0.11
Release:        1%{?dist}
Summary:        Format and parse byte quantities in human-readable units
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Number-Bytes-Human
Source0:        Number-Bytes-Human-0.11.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Carp
BuildRequires:  perl-Exporter
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators
Requires:       perl(Test::More)

%description
Number::Bytes::Human formats byte quantities with human-readable suffixes and
parses them back into numbers. Both binary and decimal units are supported,
with functional and object-oriented interfaces.

%prep
%autosetup -n Number-Bytes-Human-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license Human.pm
%doc README Changes
%{perl_vendorlib}/Number/Bytes/Human.pm
%{_mandir}/man3/Number::Bytes::Human.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package the fixed upstream release with its complete default test suite.
