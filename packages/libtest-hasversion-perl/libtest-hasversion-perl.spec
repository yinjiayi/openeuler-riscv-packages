# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-HasVersion
Version:        0.014
Release:        1%{?dist}
Summary:        Test that Perl modules have version numbers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-HasVersion
Source0:        Test-HasVersion-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester) >= 1.04
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.18
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl-generators
Requires:       perl(ExtUtils::MakeMaker)
Requires:       perl(Test::Builder)

%description
Test::HasVersion checks that Perl module files declare version numbers. The
distribution also includes the test_version command for checking modules in
an unpacked distribution.

%prep
%autosetup -n Test-HasVersion-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all eight upstream default files; target POD coverage must run.
%make_build test

%files
%license LICENSE
%doc README Changes
%{_bindir}/test_version
%{perl_vendorlib}/Test/HasVersion.pm
%{_mandir}/man3/Test::HasVersion.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.014-1
- Package official CPAN release with all default tests and CLI.
