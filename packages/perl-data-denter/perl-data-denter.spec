# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Denter
Version:        0.15
Release:        1%{?dist}
Summary:        Human-readable Perl data serialization
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Denter
Source0:        Data-Denter-0.15.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(diagnostics)
BuildRequires:  perl-YAML
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl
Requires:       perl(YAML)

%description
Human-readable Perl data serialization

%prep
%autosetup -p1 -n Data-Denter-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
install -Dpm 0644 Denter.pod %{buildroot}%{perl_vendorlib}/Data/Denter.pod
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license Denter.pod
%doc README Changes
%{perl_vendorlib}/Data/Denter.pm
%{perl_vendorlib}/Data/Denter.pod
%{_mandir}/man3/Data::Denter.3*

%changelog
* Thu Oct 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15-1
- Package Data::Denter with its original tests.
