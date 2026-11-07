# SPDX-License-Identifier: Apache-2.0
Name:           perl-Tie-ToObject
Version:        0.03
Release:        1%{?dist}
Summary:        Perl tie constructor for reusing an existing object
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-ToObject
Source0:        Tie-ToObject-0.03.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Carp
BuildRequires:  perl-generators
Requires:       perl-Scalar-List-Utils
Requires:       perl-Carp

%description
Tie::ToObject ties a Perl variable to an existing blessed object without
invoking that object's tie constructor again.

%prep
%autosetup -n Tie-ToObject-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license lib/Tie/ToObject.pm
%{perl_vendorlib}/Tie/ToObject.pm
%{_mandir}/man3/Tie::ToObject.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package the pinned official release and preserve its complete default tests.
