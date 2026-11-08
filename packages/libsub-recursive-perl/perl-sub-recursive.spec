# SPDX-License-Identifier: Apache-2.0
Name:           perl-sub-recursive
Version:        0.05
Release:        1%{?dist}
Summary:        Declare recursive and mutually recursive Perl subroutines
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Sub-Recursive
Source0:        Sub-Recursive-0.05.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.45
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
Requires:       perl
Requires:       perl(base)
Requires:       perl(Exporter)
Requires:       perl(strict)

%description
Sub::Recursive declares recursive and mutually recursive Perl subroutines
without a closure holding a reference to itself.

%prep
%autosetup -n Sub-Recursive-%{version} -p1

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
%doc README Changes
%{perl_vendorlib}/Sub/Recursive.pm
%{_mandir}/man3/Sub::Recursive.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package Sub::Recursive 0.05 with its original default tests.
