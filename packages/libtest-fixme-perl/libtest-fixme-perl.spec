# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-Fixme
Version:        0.17
Release:        1%{?dist}
Summary:        Check project files for unresolved FIXME markers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Fixme
Source0:        Test-Fixme-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(ExtUtils::Manifest)
Requires:       perl(Test::Builder)

%description
Test::Fixme scans project files for unresolved FIXME markers and reports
them through Perl's test harness.

%prep
%autosetup -n Test-Fixme-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all ten original default files, including skip_all.t's deliberate skip.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Fixme.pm
%{_mandir}/man3/Test::Fixme.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Package official CPAN release with complete default test suite.
