# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Path-Expand
Version:        1.02
Release:        1%{?dist}
Summary:        Perl module for expanding user home paths
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Path-Expand
Source0:        File-Path-Expand-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)

%description
File::Path::Expand expands tilde-prefixed file paths using HOME or the
system user database.

%prep
%autosetup -n File-Path-Expand-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the entire upstream default suite; its five penfold-host-only cases
# self-skip on every other host and are not counted as target passes.
%make_build test

%files
%doc Changes
%{perl_vendorlib}/File/Path/Expand.pm
%{_mandir}/man3/File::Path::Expand.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.02-1
- Package the official stable CPAN release and unchanged upstream tests.
