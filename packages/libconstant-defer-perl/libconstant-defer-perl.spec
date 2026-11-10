# SPDX-License-Identifier: Apache-2.0
Name:           libconstant-defer-perl
Version:        6
Release:        1%{?dist}
Summary:        Define Perl constants whose values are computed once on demand
License:        GPL-3.0-or-later
URL:            https://metacpan.org/dist/constant-defer
Source0:        constant-defer-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test)
BuildRequires:  perl(lib)
BuildRequires:  perl(vars)
BuildRequires:  perl(strict)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(vars)

%description
Define Perl constants whose values are calculated the first time they are
used and retained for subsequent calls.

%prep
%autosetup -n constant-defer-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test TEST_VERBOSE=1

%files
%license COPYING
%doc README Changes
%{perl_vendorlib}/constant/defer.pm
%{_mandir}/man3/constant::defer.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6-1
- Package the signed upstream source with all unchanged default tests.
