# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-MethodMaker
Version:        2.25
Release:        1%{?dist}
Summary:        Generate Perl object methods
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Class-MethodMaker
Source0:        Class-MethodMaker-2.25.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(IPC::Run)
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Env)
BuildRequires:  perl(Fatal)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(POSIX)
BuildRequires:  perl-generators
Requires:       perl

%description
Generate Perl object methods

%prep
%autosetup -p1 -n Class-MethodMaker-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}"
%make_build

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorarch}/Class/MethodMaker.pm
%{perl_vendorarch}/Class/MethodMaker/
%{perl_vendorarch}/auto/Class/MethodMaker/
%{_mandir}/man3/Class::MethodMaker*.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.25-1
- Package Class::MethodMaker with its original tests.
