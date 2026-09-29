# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Tail
Version:        1.3
Release:        1%{?dist}
Summary:        Read growing log files with Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Tail
Source0:        File-Tail-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(IO::Seekable)
BuildRequires:  perl(Time::HiRes)

%description
File::Tail follows growing files, including files that are reopened or
rotated, through a Perl API.

%prep
%autosetup -n File-Tail-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all three default upstream suites, including rotation/name-change.
%make_build test

%files
%doc Changes README
%{perl_vendorlib}/File/Tail.pm
%{_mandir}/man3/File::Tail.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Package the official stable CPAN release and all upstream test files.
