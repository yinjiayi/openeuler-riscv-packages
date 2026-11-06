# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-CounterFile
Version:        1.04
Release:        1%{?dist}
Summary:        Persistent file-backed counters with locking for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-CounterFile
Source0:        File-CounterFile-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Config)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(Symbol)
Requires:       perl(Carp)
Requires:       perl(Fcntl)
Requires:       perl(Symbol)

%description
File::CounterFile stores a counter in a file and uses file locking to keep
updates consistent among cooperating Perl processes.

%prep
%autosetup -n File-CounterFile-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep both upstream default suites, including 100 fork/flock race rounds.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/File/CounterFile.pm
%{_mandir}/man3/File::CounterFile.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.04-1
- Package official CPAN source and retain both default upstream tests.
