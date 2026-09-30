# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Copy-Link
Version:        0.200
Release:        1%{?dist}
Summary:        Replace a symbolic link with a copy of its target in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Copy-Link
Source0:        File-Copy-Link-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)

%description
File::Copy::Link replaces a symbolic link with a copy of its target.
File::Spec::Link resolves linked paths. The copylink command provides the
same operation for shell use.

%prep
%autosetup -n File-Copy-Link-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all nine default upstream suites, including the command-line and POD
# tests. The POD modules are BuildRequires to prevent optional skips.
%make_build test

%files
%doc Changes README CONTRIBUTING
%{perl_vendorlib}/File/Copy/Link.pm
%{perl_vendorlib}/File/Spec/Link.pm
%{_bindir}/copylink
%{_mandir}/man1/copylink.1*
%{_mandir}/man3/File::Copy::Link.3*
%{_mandir}/man3/File::Spec::Link.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.200-1
- Package the official stable CPAN release and all nine upstream suites.
