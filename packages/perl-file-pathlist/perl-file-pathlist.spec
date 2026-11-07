# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-file-pathlist
Version:        1.04
Release:        1%{?dist}
Summary:        Find a file within an ordered list of paths in Perl
License:        GPL-1.0-or-later
URL:            https://metacpan.org/dist/File-PathList
Source0:        File-PathList-%{version}.tar.gz
Patch0:         0001-retain-module-install-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Params-Util >= 0.24
BuildRequires:  perl-PathTools >= 0.80
BuildRequires:  perl-File-Path
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl-Params-Util >= 0.24
Requires:       perl-PathTools >= 0.80

%description
File::PathList searches ordered filesystem paths for a relative filename,
with optional caching of resolved results.

%prep
%setup -q -n File-PathList-%{version}
%patch -P 0 -p1

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license LICENSE NOTICE.ModuleInstall
%doc README Changes
%{perl_vendorlib}/File/PathList.pm
%{_mandir}/man3/File::PathList.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Retain original default tests and restore bundled helper notices.
