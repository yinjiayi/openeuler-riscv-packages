# SPDX-License-Identifier: Apache-2.0
Name:           perl-package-new
Version:        0.10
Release:        1%{?dist}
Summary:        Simple base package from which Perl objects inherit
License:        BSD-3-Clause
URL:            https://metacpan.org/dist/Package-New
Source0:        Package-New-0.10.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::Simple) >= 0.44
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Devel::Hide)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Package::New provides a consistent constructor and a customizable
initializer for Perl objects. Package::New::Dump adds optional object
serialization through Data::Dumper.

%prep
%autosetup -n Package-New-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc README.md Changes
%dir %{perl_vendorlib}/Package
%dir %{perl_vendorlib}/Package/New
%{perl_vendorlib}/Package/New.pm
%{perl_vendorlib}/Package/New/Dump.pm
%{_mandir}/man3/Package::New.3*
%{_mandir}/man3/Package::New::Dump.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10-1
- Package Package::New 0.10 with its original license and default tests.
