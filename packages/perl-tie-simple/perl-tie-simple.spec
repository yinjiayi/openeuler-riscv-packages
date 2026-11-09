# SPDX-License-Identifier: Apache-2.0
Name:           perl-tie-simple
Version:        1.04
Release:        1%{?dist}
Summary:        Tie Perl variables to callback-based implementations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-Simple
Source0:        Tie-Simple-%{version}.tar.gz
Patch0:         0001-retain-dist-zilla-template-notice.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl

%description
Tie::Simple connects Perl scalars, arrays, hashes and handles to callback
implementations without requiring a separate class for each tie.

%prep
%setup -q -n Tie-Simple-%{version}
%global _default_patch_fuzz 0
%patch -P 0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license LICENSE NOTICE.Dist-Zilla
%doc README Changes
%{perl_vendorlib}/Tie/Simple.pm
%{perl_vendorlib}/Tie/Simple/
%{_mandir}/man3/Tie::Simple.3pm*
%{_mandir}/man3/Tie::Simple::*.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Package the fixed release with its unchanged default tests and generator notice.
