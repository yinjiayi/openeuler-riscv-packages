# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-ConfigDir
Version:        0.021
Release:        1%{?dist}
Summary:        Discover configuration file directories in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-ConfigDir
Source0:        File-ConfigDir-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-File-Path
BuildRequires:  perl-File-Temp
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Without-Module
BuildRequires:  perl-generators

%description
File::ConfigDir discovers system, vendor, site and user configuration
directories and allows applications to register additional sources.

%prep
%autosetup -n File-ConfigDir-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the full six-file default upstream suite (60 assertions).
%make_build test

%files
%license LICENSE GPL-1 ARTISTIC-1.0
%doc README.md Changes
%{perl_vendorlib}/File/ConfigDir.pm
%{_mandir}/man3/File::ConfigDir.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.021-1
- Package official CPAN release with its complete upstream test suite.
