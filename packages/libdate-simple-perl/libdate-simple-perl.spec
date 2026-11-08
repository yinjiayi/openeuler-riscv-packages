# SPDX-License-Identifier: Apache-2.0
Name:           libdate-simple-perl
Version:        3.03
Release:        1%{?dist}
Summary:        Work with Gregorian calendar dates in Perl
License:        GPL-2.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Date-Simple
Source0:        Date-Simple-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(warnings::register)
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Carp)
BuildRequires:  perl(overload)
BuildRequires:  perl(DynaLoader)
Requires:       perl
Requires:       perl(Scalar::Util)

%description
Date::Simple provides Gregorian calendar date objects, arithmetic, and
ISO formatting. This package builds the upstream native XS implementation.

%prep
%autosetup -n Date-Simple-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%make_build
test -s blib/arch/auto/Date/Simple/Simple.so

%install
make pure_install DESTDIR=%{buildroot}

%check
# The complete unchanged upstream suite runs with a deterministic timezone.
TZ=UTC make test TEST_VERBOSE=1

%files
%license COPYING README
%doc ChangeLog
%{perl_vendorarch}/Date/Simple.pm
%{perl_vendorarch}/Date/Simple/
%{perl_vendorarch}/auto/Date/Simple/
%{_mandir}/man3/Date::Simple.3pm*
%{_mandir}/man3/Date::Simple::D8.3pm*
%{_mandir}/man3/Date::Simple::Fmt.3pm*
%{_mandir}/man3/Date::Simple::ISO.3pm*
%{_mandir}/man3/Date::Simple::NoXS.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.03-1
- Package the fixed upstream release with native XS and all default tests.
