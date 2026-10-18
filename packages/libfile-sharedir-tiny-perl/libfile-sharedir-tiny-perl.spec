# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-ShareDir-Tiny
Version:        0.001
Release:        1%{?dist}
Summary:        Locate shared files for Perl modules and distributions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-ShareDir-Tiny
Source0:        File-ShareDir-Tiny-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::ShareDir::Tiny locates installed shared data directories and files
associated with Perl modules and distributions.

%prep
%autosetup -n File-ShareDir-Tiny-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all three default upstream tests, including compile and failure cases.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/ShareDir/Tiny.pm
%{_mandir}/man3/File::ShareDir::Tiny.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.001-1
- Package official CPAN release with all default upstream tests.
