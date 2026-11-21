# SPDX-License-Identifier: Apache-2.0
Name:           perl-tie-function
Version:        0.02
Release:        1%{?dist}
Summary:        Call a Perl function through a tied hash lookup
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-Function
Source0:        Tie-Function-0.02.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  make
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test)
BuildRequires:  sed
BuildRequires:  findutils
Requires:       perl
Requires:       perl(Carp)

%description
Tie::Function lets a tied Perl hash look up a value by calling a function.

%prep
%autosetup -n Tie-Function-%{version} -p1
sed -n '/^Copyright (C) 2004,2005 david nicol /{p;n;p;}' Function.pm > LICENSE.upstream
test -s LICENSE.upstream

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE.upstream
%{perl_vendorlib}/Tie/Function.pm
%{_mandir}/man3/Tie::Function.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package Tie::Function 0.02 with the original test.pl and author notice.
