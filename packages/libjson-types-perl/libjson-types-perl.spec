# SPDX-License-Identifier: Apache-2.0
Name:           perl-JSON-Types
Version:        0.05
Release:        1%{?dist}
Summary:        Explicit scalar type helpers for JSON encoding
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/JSON-Types
Source0:        JSON-Types-0.05.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(JSON)
BuildRequires:  perl(Module::Install)
BuildRequires:  perl(Module::Install::AuthorTests)
BuildRequires:  perl(Module::Install::ReadmeFromPod)
BuildRequires:  perl(Module::Install::Repository)
BuildRequires:  perl-generators
Requires:       perl
BuildArch:      noarch

%description
Explicit scalar type helpers for JSON encoding

%prep
%autosetup -p1 -n JSON-Types-%{version}

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/JSON/Types.pm
%{_mandir}/man3/JSON::Types.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package JSON::Types with its original test suite.
