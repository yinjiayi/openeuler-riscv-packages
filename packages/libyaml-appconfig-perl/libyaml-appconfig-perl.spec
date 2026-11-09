# SPDX-License-Identifier: Apache-2.0
Name:           libyaml-appconfig-perl
Version:        0.19
Release:        1%{?dist}
Summary:        Manage YAML configuration with variable interpolation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/YAML-AppConfig
Source0:        YAML-AppConfig-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(YAML) >= 0.38
BuildRequires:  perl(Carp)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(YAML) >= 0.38

%description
Read, interpolate and write YAML configuration using variable references.

%prep
%setup -q -n YAML-AppConfig-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
# Upstream uses relative do for its own fixture. Add only this verified
# absolute source root, only to the unmodified default test invocation.
PERL_USE_UNSAFE_INC=0 PERL5LIB="$(pwd -P)" make test

%files
%license LICENSE
%doc README.md Changes
%{perl_vendorlib}/YAML/AppConfig.pm
%{_mandir}/man3/YAML::AppConfig.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.19-1
- Package the fixed upstream release with the complete original test suite.
