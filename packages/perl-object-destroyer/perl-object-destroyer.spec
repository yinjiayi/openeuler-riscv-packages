# SPDX-License-Identifier: Apache-2.0
Name:           perl-Object-Destroyer
Version:        2.02
Release:        1%{?dist}
Summary:        Perl scoped cleanup handles for circular object references
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0 AND Artistic-2.0
URL:            https://metacpan.org/dist/Object-Destroyer
Source0:        Object-Destroyer-2.02.tar.gz
Patch0:         0001-retain-generated-helper-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Carp
BuildRequires:  perl-PathTools
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-CPAN-Meta
BuildRequires:  perl-generators
Requires:       perl-Carp
Requires:       perl-Scalar-List-Utils

%description
Object::Destroyer provides lexically scoped cleanup handles for objects and
code references, including circular references and transparent wrappers.

%prep
%setup -q -n Object-Destroyer-%{version}
%patch -P 0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install

%check
# Preserve the original default t/*.t selection and propagate all failures.
%make_build test

%files
%license LICENSE LICENSE.generated
%doc Changes
%{perl_vendorlib}/Object/Destroyer.pm
%{_mandir}/man3/Object::Destroyer.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.02-1
- Package the official fixed release and retain generated helper notices.
