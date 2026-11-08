# SPDX-License-Identifier: Apache-2.0
Name:           libtest-manifest-perl
Version:        2.026
Release:        1%{?dist}
Summary:        Select and order Perl tests using a test manifest
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Test-Manifest
Source0:        Test-Manifest-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(version) >= 0.86
Requires:       perl
Requires:       perl(File::Spec)
Requires:       perl(File::Spec::Functions)
Requires:       perl(Test::Harness)

%description
Test::Manifest lets Perl projects select and order tests using a manifest.
It supports test levels and included manifest files.

%prep
%autosetup -n Test-Manifest-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Exercise all original tests, including the POD and POD coverage checks.
make test TEST_VERBOSE=1

%files
%license LICENSE
%doc README.pod Changes
%{perl_vendorlib}/Test/Manifest.pm
%{_mandir}/man3/Test::Manifest.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.026-1
- Package the official CPAN release and run the original default tests.
