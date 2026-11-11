# SPDX-License-Identifier: Apache-2.0
Name:           perl-IO-Prompt-Tiny
Version:        0.003
Release:        1%{?dist}
Summary:        Prompt for user input with a default option
License:        Apache-2.0
URL:            https://metacpan.org/release/IO-Prompt-Tiny
Source0:        IO-Prompt-Tiny-0.003.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl-generators
Requires:       perl
BuildArch:      noarch

%description
Prompt for user input with a default option

%prep
%autosetup -p1 -n IO-Prompt-Tiny-%{version}

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
%{perl_vendorlib}/IO/Prompt/Tiny.pm
%{_mandir}/man3/IO::Prompt::Tiny.3*

%changelog
* Sat Oct 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.003-1
- Package IO::Prompt::Tiny with its original tests.
