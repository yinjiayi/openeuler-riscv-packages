# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Share
Version:        0.27
Release:        1%{?dist}
Summary:        Resolve shared files in local Perl libraries
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Share
Source0:        File-Share-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-File-ShareDir >= 1.03
BuildRequires:  perl-Readonly >= 2.05
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl-File-ShareDir >= 1.03
Requires:       perl-Readonly >= 2.05

%description
File::Share extends File::ShareDir with lookup of shared files in local
Perl library trees as well as installed distributions.

%prep
%autosetup -n File-Share-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all three default t files; author POD test is upstream conditional.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/Share.pm
%{perl_vendorlib}/File/Share.pod
%{_mandir}/man3/File::Share.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.27-1
- Package official CPAN release and its complete default test pattern.
