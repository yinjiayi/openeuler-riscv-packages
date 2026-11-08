# SPDX-License-Identifier: Apache-2.0
Name:           perl-number-tolerant
Version:        1.710
Release:        1%{?dist}
Summary:        Tolerance ranges for inexact Perl numbers
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0
URL:            https://metacpan.org/dist/Number-Tolerant
Source0:        Number-Tolerant-1.710.tar.gz
Patch0:         0001-preserve-helper-notices.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Sub::Exporter) >= 0.950
BuildRequires:  perl(Sub::Exporter::Util)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  make
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.78
BuildRequires:  perl-generators
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Tester)
BuildRequires:  perl(base)
BuildRequires:  perl(if)
BuildRequires:  perl(feature)
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(Carp)
Requires:       perl(Math::BigFloat)
Requires:       perl(Math::BigRat)
Requires:       perl(Scalar::Util)
Requires:       perl(Sub::Exporter) >= 0.950
Requires:       perl(Sub::Exporter::Util)
Requires:       perl(Test::Builder)
Requires:       perl(overload)
Requires:       perl(parent)

%description
Number::Tolerant represents ranges of acceptable values for inexact numbers.
Test::Tolerant adds an assertion that checks a value against such a range.

%prep
%autosetup -n Number-Tolerant-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE GENERATED-HELPER-NOTICES GENERATED-HELPER-APACHE-LICENSE
%doc README Changes
%{perl_vendorlib}/Number/Tolerant.pm
%{perl_vendorlib}/Number/Tolerant/
%{perl_vendorlib}/Test/Tolerant.pm
%{_mandir}/man3/Number::Tolerant*.3*
%{_mandir}/man3/Test::Tolerant.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.710-1
- Package Number::Tolerant 1.710 with original tests and helper notices.
