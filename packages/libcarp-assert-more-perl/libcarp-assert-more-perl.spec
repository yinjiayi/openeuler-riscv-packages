# SPDX-License-Identifier: Apache-2.0
Name:           libcarp-assert-more-perl
Version:        2.9.0
Release:        1%{?dist}
Summary:        Assert program conditions in Perl with useful error messages
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Carp-Assert-More
Source0:        Carp-Assert-More-%{version}.tar.gz
Source1:        Artistic-2.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(Carp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More) >= 0.72
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(DateTime)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Scalar::Util)

%description
Carp::Assert::More checks conditions such as types, ranges, and calling
context, and reports a useful exception when an assertion fails.

%prep
%autosetup -n Carp-Assert-More-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
install -pm0644 %{SOURCE1} Artistic-2.0.txt

%check
make test TEST_VERBOSE=1

%files
%license README.md Artistic-2.0.txt
%doc Changes
%{perl_vendorlib}/Carp/Assert/More.pm
%{_mandir}/man3/Carp::Assert::More.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.9.0-1
- Package the fixed upstream release with all default tests and full license text.
