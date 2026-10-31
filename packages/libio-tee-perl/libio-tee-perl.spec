# SPDX-License-Identifier: Apache-2.0
Name:           perl-IO-Tee
Version:        0.66
Release:        1%{?dist}
Summary:        Multiplex output to multiple output handles
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/IO-Tee
Source0:        IO-Tee-0.66.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
Requires:       perl
BuildArch:      noarch

%description
Multiplex output to multiple output handles

%prep
%autosetup -p1 -n IO-Tee-%{version}

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
%{perl_vendorlib}/IO/Tee.pm
%{_mandir}/man3/IO::Tee.3*

%changelog
* Sat Oct 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.66-1
- Package IO::Tee with its original test suite.
