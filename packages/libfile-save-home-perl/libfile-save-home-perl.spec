# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Save-Home
Version:        0.12
Release:        1%{?dist}
Summary:        Temporarily save and restore files under a home directory
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-Save-Home
Source0:        File-Save-Home-0.12.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Simple)
BuildRequires:  perl(String::Random)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Cwd)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl

%description
Temporarily save and restore files under a home directory

%prep
%autosetup -p1 -n File-Save-Home-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/Save/Home.pm
%{_mandir}/man3/File::Save::Home.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Package File::Save::Home with its original tests.
