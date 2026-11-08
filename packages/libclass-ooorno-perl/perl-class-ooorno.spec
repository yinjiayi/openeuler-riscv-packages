# SPDX-License-Identifier: Apache-2.0
Name:           perl-class-ooorno
Version:        0.011
Release:        1%{?dist}
Summary:        Handle object-oriented and functional Perl arguments uniformly
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-OOorNO
Source0:        Class-OOorNO-0.011.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  make
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test)
BuildRequires:  perl(lib)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(strict)
Requires:       perl(vars)
Requires:       perl(Exporter)
Requires:       perl(UNIVERSAL)

%description
Class::OOorNO lets Perl routines handle object-oriented and functional calls
and separate options from positional arguments.

%prep
%autosetup -n Class-OOorNO-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license COPYING README
%doc Changes
%{perl_vendorlib}/Class/OOorNO.pm
%{perl_vendorlib}/Class/OOorNO.pod
%{_mandir}/man3/Class::OOorNO.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.011-1
- Package Class::OOorNO 0.011 and run its original default suite.
