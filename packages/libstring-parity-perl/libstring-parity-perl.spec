# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Parity
Version:        1.34
Release:        1%{?dist}
Summary:        Manipulate byte parity in Perl strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Parity
Source0:        String-Parity-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
String::Parity sets and checks even, odd, mark and space parity on bytes in
Perl strings, and counts or displays byte parity states.

%prep
%autosetup -n String-Parity-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the sole unmodified upstream default suite: 33 byte-parity checks.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/String/Parity.pm
%{_mandir}/man3/String::Parity.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.34-1
- Package official CPAN release with the full default parity test suite.
