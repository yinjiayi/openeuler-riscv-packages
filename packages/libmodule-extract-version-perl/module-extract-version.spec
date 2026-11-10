# SPDX-License-Identifier: Apache-2.0
Name:           perl-module-extract-version
Version:        1.123
Release:        1%{?dist}
Summary:        Extract a Perl module version from source
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Module-Extract-VERSION
Source0:        Module-Extract-VERSION-1.123.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(utf8)
BuildRequires:  perl(Tie::Hash::NamedCapture)
BuildRequires:  perl(version) >= 0.77
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(utf8)
Requires:       perl(Tie::Hash::NamedCapture)
Requires:       perl(version) >= 0.77

%description
Module::Extract::VERSION reads a Perl module source file and extracts its
version string without loading that module.

%prep
%autosetup -n Module-Extract-VERSION-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc README.pod Changes
%{perl_vendorlib}/Module/Extract/VERSION.pm
%{_mandir}/man3/Module::Extract::VERSION.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.123-1
- Package the verified CPAN release and retain all default tests.
