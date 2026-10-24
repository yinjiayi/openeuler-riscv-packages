# SPDX-License-Identifier: Apache-2.0
Name:           perl-Math-Base85
Version:        0.5
Release:        1%{?dist}
Summary:        Convert arbitrary-precision integers to RFC 1924 base85 strings
License:        Artistic-1.0-Perl AND LicenseRef-RFC-1924-Verbatim
URL:            https://metacpan.org/dist/Math-Base85
Source0:        Math-Base85-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-Exporter
BuildRequires:  perl-ExtUtils-MakeMaker >= 6.64
BuildRequires:  perl-Math-BigInt
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-constant
BuildRequires:  perl-generators
Requires:       perl-Carp
Requires:       perl-Exporter
Requires:       perl-Math-BigInt
Requires:       perl-constant

%description
Math::Base85 converts arbitrary-precision integers to and from the base85
alphabet described by RFC 1924. The complete original RFC is included
unchanged under its own verbatim-distribution terms, not the code's license.

%prep
%autosetup -n Math-Base85-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the full default t/00-basic.t and all five original assertions.
%make_build test

%files
%license LICENSE README.md rfc1924.txt
%doc Changes
%{perl_vendorlib}/Math/Base85.pm
%{_mandir}/man3/Math::Base85.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5-1
- Package original source and whole RFC with full default tests and smoke.
