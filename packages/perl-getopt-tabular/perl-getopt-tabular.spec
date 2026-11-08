# SPDX-License-Identifier: Apache-2.0
Name:           perl-getopt-tabular
Version:        0.3
Release:        1%{?dist}
Summary:        Table-driven command-line argument parsing for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Getopt-Tabular
Source0:        Getopt-Tabular-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Exporter
BuildRequires:  perl-Carp
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl-Exporter
Requires:       perl-Carp

%description
Getopt::Tabular parses command-line arguments using tables of option types,
argument counts and destinations, with generated help and extensible types.

%prep
%setup -q -n Getopt-Tabular-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test
# Older MakeMaker executes test.pl directly; additionally enforce its full TAP.
%{__perl} -Iblib/lib -Iblib/arch -MTest::Harness -e 'runtests("test.pl")'

%files
%license README
%doc Changes demo
%{perl_vendorlib}/Getopt/Tabular.pm
%{perl_vendorlib}/Getopt/Tabular.pod
%{_mandir}/man3/Getopt::Tabular.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3-1
- Package the original default tests with additional full TAP enforcement.
