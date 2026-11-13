# SPDX-License-Identifier: Apache-2.0
Name:           perl-sort-fields
Version:        1.003
Release:        1%{?dist}
Summary:        Sort strings by selected fields
License:        Artistic-2.0
URL:            https://metacpan.org/release/BRIANDFOY/Sort-Fields-1.003
Source0:        Sort-Fields-1.003.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(version) >= 0.86
BuildRequires:  perl(warnings)
%description
Sort::Fields sorts strings by selected numeric or lexicographic fields,
with an optional stable order for ties.

%prep
%autosetup -n Sort-Fields-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test TEST_VERBOSE=1

%files
%license LICENSE
%doc README.pod Changes SECURITY.md
%{perl_vendorlib}/Sort/Fields.pm
%{_mandir}/man3/Sort::Fields.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.003-1
- Package the fixed CPAN release with the original default tests.
