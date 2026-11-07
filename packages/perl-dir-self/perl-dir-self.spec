# SPDX-License-Identifier: Apache-2.0
Name:           perl-Dir-Self
Version:        0.11
Release:        1%{?dist}
Summary:        Perl source-file directory pseudo-constant
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Dir-Self
Source0:        Dir-Self-0.11.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Carp
BuildRequires:  perl-PathTools
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators


%description
Dir::Self provides a __DIR__ pseudo-constant for the absolute directory of
the current Perl source file, including modules. Static imports are supported.

%prep
%autosetup -n Dir-Self-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license lib/Dir/Self.pm
%doc README Changes
%{perl_vendorlib}/Dir/Self.pm
%{_mandir}/man3/Dir::Self.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package the official release with the complete upstream default tests.
