# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Monitor
Version:        1.00
Release:        1%{?dist}
Summary:        Poll files and directories for changes in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Monitor
Source0:        File-Monitor-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Module::Build) >= 0.36
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(version)
Requires:       perl(Carp)
Requires:       perl(Fcntl)
Requires:       perl(File::Spec)
Requires:       perl(Scalar::Util)

%description
File::Monitor polls files and directories and reports changes to their
contents and metadata between scans.

%prep
%autosetup -n File-Monitor-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all eight default t/*.t tests while isolating their fmtest-$$ IO.
test_tmp="$(mktemp -d "$PWD/monitor-tests.XXXXXX")"
TMPDIR="$test_tmp" %make_build test
rmdir "$test_tmp"

%files
%doc README Changes
%{perl_vendorlib}/File/Monitor.pm
%{perl_vendorlib}/File/Monitor/
%{_mandir}/man3/File::Monitor*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.00-1
- Package official CPAN source and preserve all default upstream tests.
