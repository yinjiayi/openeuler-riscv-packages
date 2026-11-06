# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Path-Tiny
Version:        1.0
Release:        1%{?dist}
Summary:        Small recursive directory creation and removal for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Path-Tiny
Source0:        File-Path-Tiny-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Temp)

%description
File::Path::Tiny implements recursive directory creation and removal with
checks that avoid following a directory replaced by a symbolic link.

%prep
%autosetup -n File-Path-Tiny-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all nine upstream default test files. The two functional files must
# execute 52 assertions; seven author tests skip by upstream RELEASE_TESTING
# policy. Do not let the symlink-safety test silently skip for missing tools.
test -x /bin/mv
test -x /bin/mkdir
%make_build test

%files
%license lib/File/Path/Tiny.pod
%doc README Changes
%{perl_vendorlib}/File/Path/Tiny.pm
%{perl_vendorlib}/File/Path/Tiny.pod
%{_mandir}/man3/File::Path::Tiny.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0-1
- Package official CPAN release with its unchanged default test suite.
