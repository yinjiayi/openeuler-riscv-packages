# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-carp
Version:        0.2
Release:        1%{?dist}
Summary:        Test for calls to Perl Carp functions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Carp
Source0:        Test-Carp-0.2.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More)
BuildRequires:  make
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(Carp)
Requires:       perl(Data::Dumper)
Requires:       perl(Test::More)

%description
Test::Carp checks whether Perl code calls a Carp function, optionally matching
the warning or exception message.

%prep
%autosetup -n Test-Carp-%{version} -p1

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
%{perl_vendorlib}/Test/Carp.pm
%{_mandir}/man3/Test::Carp.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2-1
- Package Test::Carp 0.2 with the original default test suite.
