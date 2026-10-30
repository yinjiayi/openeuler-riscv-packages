# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Phrasebook
Version:        0.35
Release:        1%{?dist}
Summary:        Access data using the phrasebook design pattern
License:        Artistic-2.0
URL:            https://metacpan.org/release/Data-Phrasebook
Source0:        Data-Phrasebook-0.35.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Module::Pluggable)
BuildArch:      noarch

%description
Access data using the phrasebook design pattern

%prep
%autosetup -p1 -n Data-Phrasebook-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes ChangeLog
%{perl_vendorlib}/Data/Phrasebook.pm
%{perl_vendorlib}/Data/Phrasebook/
%{_mandir}/man3/Data::Phrasebook*.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.35-1
- Package Data::Phrasebook with its original test suite.
