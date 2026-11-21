# SPDX-License-Identifier: Apache-2.0
Name:           perl-module-extract-namespaces
Version:        1.026
Release:        1%{?dist}
Summary:        Extract declared namespaces from Perl source
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Module-Extract-Namespaces
Source0:        Module-Extract-Namespaces-1.026.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(PPI) >= 1.270
BuildRequires:  make
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(version)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(Carp)
Requires:       perl(File::Spec::Functions)
Requires:       perl(PPI) >= 1.270

%description
Module::Extract::Namespaces uses PPI to read Perl source and report its
declared package names without executing the source.

%prep
%autosetup -n Module-Extract-Namespaces-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc README.pod Changes
%{perl_vendorlib}/Module/Extract/Namespaces.pm
%{_mandir}/man3/Module::Extract::Namespaces.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.026-1
- Package Module::Extract::Namespaces 1.026 with the original default tests.
