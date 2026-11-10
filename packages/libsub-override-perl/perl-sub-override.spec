# SPDX-License-Identifier: Apache-2.0
Name:           perl-sub-override
Version:        0.12
Release:        1%{?dist}
Summary:        Temporarily replace a Perl subroutine and restore its original behavior
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Sub-Override
Source0:        Sub-Override-0.12.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Scalar::Util) >= 1.11
BuildRequires:  perl(Carp)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(Scalar::Util) >= 1.11
Requires:       perl(Carp)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Sub::Override replaces a named Perl subroutine while retaining the
original so it can be restored.

%prep
%autosetup -n Sub-Override-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license lib/Sub/Override.pm
%doc README README.md Changes
%{perl_vendorlib}/Sub/Override.pm
%{_mandir}/man3/Sub::Override.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Package Sub::Override 0.12 with its original default tests.
