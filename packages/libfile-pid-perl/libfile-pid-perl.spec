# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Pid
Version:        1.01
Release:        1%{?dist}
Summary:        Perl PID file manipulation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Pid
Source0:        File-Pid-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(Class::Accessor::Fast) >= 0.19
Requires:       perl(Class::Accessor::Fast) >= 0.19

%description
File::Pid provides methods for writing, inspecting and removing PID files.

%prep
%autosetup -n File-Pid-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The original tests use fixed names and unlink files under File::Spec::tmpdir.
mkdir test-private-tmp
export TMPDIR="$PWD/test-private-tmp"
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/File/Pid.pm
%{_mandir}/man3/File::Pid.3*

%changelog
* Sun Nov 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.01-1
- Package official CPAN release with original tests.
