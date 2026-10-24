# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-Version
Version:        2.09
Release:        1%{?dist}
Summary:        Test that Perl module versions are sane
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Test-Version
Source0:        Test-Version-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(File::Find::Rule::Perl)
BuildRequires:  perl(Module::Metadata) >= 1.000020
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Tester)
BuildRequires:  perl(parent)
BuildRequires:  perl(version) >= 0.86
BuildRequires:  perl-generators
Requires:       perl(File::Find::Rule::Perl)
Requires:       perl(Module::Metadata) >= 1.000020
Requires:       perl(Test::Builder)
Requires:       perl(Test::More) >= 0.94
Requires:       perl(parent)
Requires:       perl(version) >= 0.86

%description
Test::Version verifies that Perl modules declare sensible, consistent
versions. It can check one source file or all modules under a directory.

%prep
%autosetup -n Test-Version-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all 21 upstream default t/*.t files; mswin32.t self-skips off Windows.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Version.pm
%{_mandir}/man3/Test::Version.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.09-1
- Package the official CPAN release with all default upstream tests.
