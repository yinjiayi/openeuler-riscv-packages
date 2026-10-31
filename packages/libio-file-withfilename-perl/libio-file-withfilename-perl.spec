# SPDX-License-Identifier: Apache-2.0
Name:           perl-IO-File-WithFilename
Version:        0.01
Release:        1%{?dist}
Summary:        IO::File handle retaining its filename
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/IO-File-WithFilename
Source0:        IO-File-WithFilename-0.01.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::File)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(File::Temp)
Requires:       perl(IO::File)
BuildArch:      noarch

%description
IO::File handle retaining its filename

%prep
%autosetup -p1 -n IO-File-WithFilename-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license lib/IO/File/WithFilename.pm
%doc README Changes
%{perl_vendorlib}/IO/File/WithFilename.pm
%{_mandir}/man3/IO::File::WithFilename.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package IO::File::WithFilename with its original test suite.
