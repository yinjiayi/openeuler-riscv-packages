# SPDX-License-Identifier: Apache-2.0
Name:           perl-object-tiny
Version:        1.09
Release:        1%{?dist}
Summary:        Minimal Perl class builder with read-only accessors
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Object-Tiny
Source0:        Object-Tiny-1.09.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-PathTools
BuildRequires:  perl-CPAN-Meta
BuildRequires:  perl-generators


%description
Object::Tiny provides a small constructor and generated read-only accessors
for Perl classes while respecting existing superclass relationships.

%prep
%autosetup -n Object-Tiny-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Object/Tiny.pm
%{_mandir}/man3/Object::Tiny.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.09-1
- Package the fixed official release with the complete default tests.
