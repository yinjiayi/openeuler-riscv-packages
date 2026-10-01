# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Modified
Version:        0.10
Release:        1%{?dist}
Summary:        Perl module for detecting changes to files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Modified
Source0:        File-Modified-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.88

%description
File::Modified records file signatures and reports whether the files have
changed, using modification times or available digest methods.

%prep
%autosetup -n File-Modified-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the full upstream default suite, including its optional-Digest
# SKIP branches and declared TODO for deep structure comparison.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/File/Modified.pm
%{_mandir}/man3/File::Modified.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10-1
- Package the official stable CPAN release and upstream default tests.
