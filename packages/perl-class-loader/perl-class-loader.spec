# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Loader
Version:        2.03
Release:        1%{?dist}
Summary:        Load Perl modules and create objects on demand
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Class-Loader
Source0:        Class-Loader-2.03.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl

%description
Load Perl modules and create objects on demand

%prep
%autosetup -p1 -n Class-Loader-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license ARTISTIC
%doc Changes
%{perl_vendorlib}/Class/Loader.pm
%{perl_vendorlib}/Class/LoaderTest.pm
%{_mandir}/man3/Class::Loader.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.03-1
- Package Class::Loader with its original tests.
