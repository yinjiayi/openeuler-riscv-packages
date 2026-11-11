# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Sprintf-Named
Version:        0.0405
Release:        1%{?dist}
Summary:        sprintf-like function with named conversions
License:        MIT
URL:            https://metacpan.org/release/Text-Sprintf-Named
Source0:        Text-Sprintf-Named-0.0405.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl
BuildArch:      noarch

%description
sprintf-like function with named conversions

%prep
%autosetup -p1 -n Text-Sprintf-Named-%{version}

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
%doc README Changes
%{perl_vendorlib}/Text/Sprintf/Named.pm
%{_mandir}/man3/Text::Sprintf::Named.3*

%changelog
* Sat Oct 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0405-1
- Package Text::Sprintf::Named with its original tests.
