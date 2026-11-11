# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Dmp
Version:        0.242
Release:        1%{?dist}
Summary:        Dump Perl data structures as Perl code
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Data-Dmp
Source0:        Data-Dmp-0.242.tar.gz
Patch0:         0001-retain-third-party-notices.patch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Regexp::Stringify)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl
Requires:       perl(Regexp::Stringify)

%description
Dump Perl data structures as Perl code

%prep
%autosetup -p1 -n Data-Dmp-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE THIRD-PARTY-NOTICES
%doc README Changes
%{perl_vendorlib}/Data/Dmp.pm
%{_mandir}/man3/Data::Dmp.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.242-1
- Package Data::Dmp with original tests and third-party notices.
