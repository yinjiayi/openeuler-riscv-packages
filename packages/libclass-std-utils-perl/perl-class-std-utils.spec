# SPDX-License-Identifier: Apache-2.0
Name:           perl-class-std-utils
Version:        0.0.3
Release:        1%{?dist}
Summary:        Utilities for implementing inside-out Perl classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Std-Utils
Source0:        Class-Std-Utils-v0.0.3.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(strict)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(List::Util)
Requires:       perl(Scalar::Util)
Requires:       perl(strict)
Requires:       perl(version)
Requires:       perl(warnings)

%description
Utilities for implementing inside-out Perl classes

%prep
%autosetup -n Class-Std-Utils-v%{version}
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Class/Std/Utils.pm
%{_mandir}/man3/Class::Std::Utils.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.3-1
- Package the fixed release with its original default tests.
