# SPDX-License-Identifier: Apache-2.0
Name:           perl-module-versions-report
Version:        1.06
Release:        1%{?dist}
Summary:        Report the versions of Perl modules currently loaded
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Module-Versions-Report
Source0:        Module-Versions-Report-1.06.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Text::Tabs)
Requires:       perl

%description
Module::Versions::Report reports Perl and the versions of modules currently
loaded, either on demand or at process exit.

%prep
%autosetup -n Module-Versions-Report-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README
%{perl_vendorlib}/Module/Versions/Report.pm
%{_mandir}/man3/Module::Versions::Report.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.06-1
- Package Module::Versions::Report with unchanged legacy tests and license.
