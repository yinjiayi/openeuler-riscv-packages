# SPDX-License-Identifier: Apache-2.0
Name:           perl-class-unload
Version:        0.12
Release:        1%{?dist}
Summary:        Unload Perl classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/ILMARI/Class-Unload-0.12
Source0:        Class-Unload-0.12.tar.gz
Source1:        Dist-Zilla-6.033.LICENSE
Source2:        Dist-Zilla-Plugin-Test-EOL-0.19.LICENSE
Source3:        Dist-Zilla-Plugin-Test-NoTabs-0.15.LICENSE
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Class::Inspector)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(Class::Inspector)

%description
Class::Unload clears a class's symbol table and module-load entry, allowing
that class to be loaded again. It also handles Moose metadata when present.

%prep
%autosetup -n Class-Unload-%{version} -p1
mkdir -p vendor-licenses
install -pm0644 %{SOURCE1} vendor-licenses/Dist-Zilla-6.033.LICENSE
install -pm0644 %{SOURCE2} vendor-licenses/Dist-Zilla-Plugin-Test-EOL-0.19.LICENSE
install -pm0644 %{SOURCE3} vendor-licenses/Dist-Zilla-Plugin-Test-NoTabs-0.15.LICENSE

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
%{perl_vendorlib}/Class/Unload.pm
%{_mandir}/man3/Class::Unload.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Package the fixed CPAN release, original taint tests, and template terms.
