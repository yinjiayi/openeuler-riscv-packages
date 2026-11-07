# SPDX-License-Identifier: Apache-2.0
Name:           perl-class-observable
Version:        2.004
Release:        1%{?dist}
Summary:        Perl observer registration and notification for classes and objects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Observable
Source0:        https://cpan.metacpan.org/authors/id/A/AR/ARISTOTLE/Class-Observable-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Class-ISA >= 0.32
BuildRequires:  perl-Scalar-List-Utils >= 1.14
BuildRequires:  perl-threads
BuildRequires:  perl-threads-shared
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Class-ISA >= 0.32
Requires:       perl-Scalar-List-Utils >= 1.14

%description
Class::Observable lets objects and classes register observers, notify them of
events, inherit class observers and manage their lifetime.

%prep
%setup -q -n Class-Observable-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
make test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Class/Observable.pm
%{_mandir}/man3/Class::Observable.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.004-1
- Package fixed upstream release with all original default tests.
