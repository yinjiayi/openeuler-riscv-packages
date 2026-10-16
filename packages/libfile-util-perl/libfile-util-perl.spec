# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Util
Version:        4.201720
Release:        1%{?dist}
Summary:        Portable file handling tools for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Util
Source0:        File-Util-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Module::Build) >= 0.28
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test)
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Scalar::Util)
Requires:       perl(Config)
Requires:       perl(Exporter)
Requires:       perl(Fcntl)
Requires:       perl(Scalar::Util)

%description
File::Util provides portable file and directory operations, including
reading, writing, path inspection and file locking.

%prep
%autosetup -n File-Util-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every default upstream t/*.t file unchanged, including IO and flock.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/Util.pm
%{perl_vendorlib}/File/Util/
%{_mandir}/man3/File::Util*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.201720-1
- Package official CPAN release with its complete default test suite.
