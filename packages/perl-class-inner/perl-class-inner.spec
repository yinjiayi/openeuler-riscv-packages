# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Inner
Version:        0.200001
Release:        1%{?dist}
Summary:        Perl implementation of inner classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Inner
Source0:        Class-Inner-0.200001.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Carp)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl

%description
Perl implementation of inner classes

%prep
%autosetup -p1 -n Class-Inner-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Class/Inner.pm
%{_mandir}/man3/Class::Inner.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.200001-1
- Package Class::Inner with its original tests.
