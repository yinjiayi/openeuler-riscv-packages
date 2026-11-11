# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Dump-OneLine
Version:        0.080
Release:        1%{?dist}
Summary:        Dump Perl data structures as single-line strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Data-Dump-OneLine
Source0:        Data-Dump-OneLine-0.080.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Data::Dmp) >= 0.241
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl
Requires:       perl(Data::Dmp) >= 0.241

%description
Dump Perl data structures as single-line strings

%prep
%autosetup -p1 -n Data-Dump-OneLine-%{version}

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
%{perl_vendorlib}/Data/Dump/OneLine.pm
%{_mandir}/man3/Data::Dump::OneLine.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.080-1
- Package Data::Dump::OneLine with its original tests.
