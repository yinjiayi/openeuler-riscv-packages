# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-HexConvert
Version:        0.02
Release:        1%{?dist}
Summary:        Convert ASCII strings to hexadecimal and back
License:        LGPL-3.0-only
URL:            https://metacpan.org/dist/String-HexConvert
Source0:        String-HexConvert-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::HexConvert exposes Perl helpers to encode ASCII strings as
hexadecimal and decode them back.

%prep
%autosetup -n String-HexConvert-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all five upstream default files. Three author-only files explicitly
# skip unless AUTHOR_TESTING is set; do not count those skips as passes.
%make_build test

%files
%license LICENSE
%doc README
%{perl_vendorlib}/String/HexConvert.pm
%{_mandir}/man3/String::HexConvert.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package official CPAN release with unmodified default upstream tests.
