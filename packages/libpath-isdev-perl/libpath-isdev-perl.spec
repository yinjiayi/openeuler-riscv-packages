# SPDX-License-Identifier: Apache-2.0
Name:           perl-Path-IsDev
Version:        1.001003
Release:        1%{?dist}
Summary:        Detect Perl development source trees
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Path-IsDev
Source0:        Path-IsDev-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(Class::Tiny)
BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Path::Tiny)
BuildRequires:  perl(Role::Tiny)
BuildRequires:  perl(Role::Tiny::With)
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Test::Fatal)
Requires:       perl(File::HomeDir)
Requires:       perl(Path::Tiny)

%description
Path::IsDev detects whether a filesystem path resembles a Perl development
source tree using configurable heuristics.

%prep
%autosetup -n Path-IsDev-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all 39 upstream default test files, including generated compile tests.
%make_build test
test -f %{buildroot}%{perl_vendorlib}/Path/IsDev.pm
PERL5LIB=%{buildroot}%{perl_vendorlib} %{__perl} -MPath::IsDev -e 'die "unexpected version\n" unless $Path::IsDev::VERSION eq "1.001003"'

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Path/IsDev.pm
%{perl_vendorlib}/Path/IsDev/
%{_mandir}/man3/Path::IsDev*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.001003-1
- Package official CPAN release with unchanged upstream default tests.
