# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-TtyLength
Version:        0.03
Release:        1%{?dist}
Summary:        Measure terminal text length and width without ANSI escapes
License:        GPL-1.0-or-later
URL:            https://metacpan.org/dist/String-TtyLength
Source0:        String-TtyLength-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(Test2::V0)
BuildRequires:  perl(Unicode::EastAsianWidth) >= 12.0
BuildRequires:  perl-generators
Requires:       perl(Unicode::EastAsianWidth) >= 12.0

%description
String::TtyLength counts terminal text length and display width after
removing supported ANSI escape sequences.

%prep
%autosetup -n String-TtyLength-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/String/TtyLength.pm
%{_mandir}/man3/String::TtyLength.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package official CPAN release with both original default test files.
