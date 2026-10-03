# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-Bits
Version:        0.02
Release:        1%{?dist}
Summary:        Compare binary data byte by byte in Perl tests
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Test-Bits
Source0:        Test-Bits-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-List-AllUtils
BuildRequires:  perl-Test-Fatal
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl-List-AllUtils
Requires:       perl-Test-Simple

%description
Test::Bits provides bits_is, a test assertion that compares byte-oriented
data with expected numeric byte values and reports the first difference.

%prep
%autosetup -n Test-Bits-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete unchanged upstream default t/*.t suite.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Bits.pm
%{_mandir}/man3/Test::Bits.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package official CPAN release with the complete default test suite.
