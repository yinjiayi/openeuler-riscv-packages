# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-class-returnvalue
Version:        0.55
Release:        1%{?dist}
Summary:        Context-sensitive return value and error objects for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-ReturnValue
Source0:        https://cpan.metacpan.org/authors/id/J/JE/JESSE/Class-ReturnValue-%{version}.tar.gz
Patch0:         0001-preserve-helper-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Devel-StackTrace
BuildRequires:  perl-generators
BuildRequires:  findutils
BuildRequires:  patch
Requires:       perl-Test-Simple
Requires:       perl-Devel-StackTrace

%description
Class::ReturnValue provides context-sensitive success and error return values,
including arrays, error messages and optional stack traces.

%prep
%setup -q -n Class-ReturnValue-%{version}
%patch -P 0 -p1

%build
perl -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -name .packlist -delete
find %{buildroot} -name perllocal.pod -delete

%check
make test

%files
%license lib/Class/ReturnValue.pm MODULE-INSTALL-LICENSE BUNDLED-HELPER-NOTICES
%doc Changes
%{perl_vendorlib}/Class/ReturnValue.pm
%{_mandir}/man3/Class::ReturnValue.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.55-1
- Package fixed release, original tests and bundled helper notices.
