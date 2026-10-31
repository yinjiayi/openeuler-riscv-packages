# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Member
Version:        1.6
Release:        1%{?dist}
Summary:        Generate Perl class member accessors
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Member
Source0:        Class-Member-1.6.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Carp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Symbol)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl

%description
Generate Perl class member accessors

%prep
%autosetup -p1 -n Class-Member-%{version}

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
%{perl_vendorlib}/Class/Member.pm
%{perl_vendorlib}/Class/Member/
%{_mandir}/man3/Class::Member*.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Package Class::Member with its original tests.
