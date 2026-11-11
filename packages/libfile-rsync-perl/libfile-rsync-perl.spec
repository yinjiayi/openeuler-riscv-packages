# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Rsync
Version:        0.49
Release:        1%{?dist}
Summary:        Perl interface to the rsync command
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Rsync
Source0:        File-Rsync-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(IPC::Run3)
BuildRequires:  rsync >= 3.0
Requires:       perl(IPC::Run3)
Requires:       rsync

%description
File::Rsync provides a Perl interface to the rsync command, including
option construction and access to command status and error messages.

%prep
%autosetup -n File-Rsync-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the original test.pl, including real local rsync operations.
export LC_ALL=C
%make_build test

%files
%license README
%doc Changelog
%{perl_vendorlib}/File/Rsync.pm
%{_mandir}/man3/File::Rsync.3*

%changelog
* Sat Oct 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.49-1
- Package official CPAN release with its original default tests.
