# SPDX-License-Identifier: Apache-2.0
Name:           perl-class-throwable
Version:        0.13
Release:        1%{?dist}
Summary:        Lightweight structured exceptions for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Throwable
Source0:        Class-Throwable-0.13.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(Scalar::Util) >= 1.10
BuildRequires:  perl(base)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(Scalar::Util) >= 1.10
Requires:       perl(overload)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Class::Throwable defines structured Perl exceptions with messages, stack
traces and optional nested exceptions.

%prep
%autosetup -n Class-Throwable-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README
%doc Changes
%{perl_vendorlib}/Class/Throwable.pm
%{_mandir}/man3/Class::Throwable.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Package Class::Throwable 0.13 with its complete original default suite.
