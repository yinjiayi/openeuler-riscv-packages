# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-FindLib
Version:        0.001004
Release:        1%{?dist}
Summary:        Find a library relative to an ancestor of a Perl script
License:        Unlicense
URL:            https://metacpan.org/dist/File-FindLib
Source0:        File-FindLib-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::FindLib searches upward from a Perl script for a named library
directory or module file, then adds or loads the matching path.

%prep
%autosetup -n File-FindLib-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the complete three-file default upstream test suite.
%make_build test

%files
%license LICENSE
%doc Changes
%{perl_vendorlib}/File/FindLib.pm
%{_mandir}/man3/File::FindLib.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.001004-1
- Package official CPAN release with all default upstream tests.
