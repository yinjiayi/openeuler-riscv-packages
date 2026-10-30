# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-UserConfig
Version:        0.06
Release:        1%{?dist}
Summary:        Locate user configuration or copy defaults
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-UserConfig
Source0:        File-UserConfig-0.06.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Remove)
BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(File::HomeDir)
Requires:       perl(File::ShareDir)
Requires:       perl(File::Copy::Recursive)
BuildArch:      noarch

%description
Locate user configuration or copy defaults

%prep
%autosetup -p1 -n File-UserConfig-%{version}

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/UserConfig.pm
%{perl_vendorlib}/auto/share/dist/File-UserConfig/
%{_mandir}/man3/File::UserConfig.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package File::UserConfig with its original tests and shared data.
