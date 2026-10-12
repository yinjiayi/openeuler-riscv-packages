# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Slurp-Tiny
Version:        0.004
Release:        1%{?dist}
Summary:        Small legacy Perl file slurping utilities
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Slurp-Tiny
Source0:        File-Slurp-Tiny-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::Slurp::Tiny provides legacy file read, write, line, and directory
helpers. Upstream marks the distribution discouraged for new projects;
this RPM is for existing consumers that still depend on its API.

%prep
%autosetup -n File-Slurp-Tiny-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the complete default upstream test suite.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/Slurp/Tiny.pm
%{_mandir}/man3/File::Slurp::Tiny.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.004-1
- Package official CPAN release with its complete default test.
