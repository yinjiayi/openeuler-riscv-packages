# SPDX-License-Identifier: Apache-2.0
Name:           perl-set-object
Version:        1.43
Release:        1%{?dist}
Summary:        Unordered collections of Perl objects and scalars
License:        Artistic-2.0 AND Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Set-Object
Source0:        Set-Object-%{version}.tar.gz
Patch0:         0001-preserve-component-license-scope.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl-Scalar-List-Utils
Requires:       perl-Test-Simple

%description
Set::Object implements unordered collections of scalars and references using
XS, including set operations and weak sets. Upstream states it is not
thread-safe; this package does not claim otherwise.

%prep
%setup -q -n Set-Object-%{version}
%global _default_patch_fuzz 0
%patch -P 0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build OPTIMIZE="%{optflags}"

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorarch}/auto/Set/Object/Object.so

%check
make test

%files
%license LICENSE COPYING.Artistic1 NOTICE.Scope
%doc README Changes.pod examples
%{perl_vendorarch}/Set/Object.pm
%{perl_vendorarch}/Set/Object/
%{perl_vendorarch}/auto/Set/Object/
%{_mandir}/man3/Set::Object*.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.43-1
- Retain component license scope and all upstream default tests.
