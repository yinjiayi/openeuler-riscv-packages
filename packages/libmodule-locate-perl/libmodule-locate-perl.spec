# SPDX-License-Identifier: Apache-2.0
Name:           perl-module-locate
Version:        1.80
Release:        1%{?dist}
Summary:        Locate Perl modules without executing them
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/NEILB/Module-Locate-1.80
Source0:        Module-Locate-%{version}.tar.gz
Source1:        Dist-Zilla-5.037.LICENSE
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.8.8
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%description
Module::Locate finds Perl modules as require or use would find them, without
loading or executing their code.

%prep
%autosetup -n Module-Locate-%{version} -p1
mkdir -p vendor-licenses
install -pm0644 %{SOURCE1} vendor-licenses/Dist-Zilla-5.037.LICENSE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test TEST_VERBOSE=1

%files
%license LICENSE vendor-licenses/*
%doc README Changes
%{perl_vendorlib}/Module/Locate.pm
%{_mandir}/man3/Module::Locate.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.80-1
- Package the fixed upstream release with its original MakeMaker tests.
