# SPDX-License-Identifier: Apache-2.0
Name:           perl-module-util
Version:        1.09
Release:        1%{?dist}
Summary:        Find installed Perl modules and translate module names and paths
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Module-Util
Source0:        Module-Util-1.09.tar.gz
Patch0:         0001-retain-module-build-compat-notice.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.40
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  patch
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(Exporter)
Requires:       perl(File::Find)
Requires:       perl(File::Spec::Functions)
Requires:       perl(List::Util)
Requires:       perl(Pod::Usage)
Requires:       perl(Getopt::Long)
Requires:       perl-ExtUtils-MakeMaker

%description
Module::Util locates installed Perl modules and converts between module names
and file paths. The pm_which command exposes the lookup at the command line.

%prep
%autosetup -n Module-Util-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir "%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
./Build test --verbose 1

%files
%license README MODULE-BUILD-COMPAT-NOTICE
%doc Changes
%{perl_vendorlib}/Module/Util.pm
%{_bindir}/pm_which
%{_mandir}/man1/pm_which.1*
%{_mandir}/man3/Module::Util.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.09-1
- Package Module::Util 1.09 with its original suite and generated-wrapper notice.
