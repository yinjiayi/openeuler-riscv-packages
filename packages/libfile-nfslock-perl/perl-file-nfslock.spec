# SPDX-License-Identifier: Apache-2.0
Name:           perl-file-nfslock
Version:        1.29
Release:        1%{?dist}
Summary:        NFS-compatible Perl file locking helper
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-NFSLock
Source0:        File-NFSLock-1.29.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More)
BuildRequires:  /usr/bin/pod2text
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(POSIX)
Requires:       perl(Sys::Hostname)
Requires:       perl(base)
Requires:       perl(constant)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
NFS-compatible Perl file locking helper

%prep
%autosetup -n File-NFSLock-%{version}
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/File/NFSLock.pm
%{_mandir}/man3/File::NFSLock.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.29-1
- Package the fixed upstream release with its original default tests.
