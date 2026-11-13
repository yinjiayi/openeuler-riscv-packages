# SPDX-License-Identifier: Apache-2.0
Name:           perl-file-mmagic
Version:        1.30
Release:        1%{?dist}
Summary:        Identify file types using magic rules
License:        LicenseRef-PPT-file-kulp AND LicenseRef-Ian-Darwin-file AND Apache-1.0
URL:            https://metacpan.org/release/KNOK/File-MMagic-1.30
Source0:        File-MMagic-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
Requires:       perl(FileHandle)

%description
File::MMagic identifies file types from contents using a built-in
magic database or explicitly supplied rules.

%prep
%autosetup -n File-MMagic-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/File/MMagic.pm
test -f %{buildroot}%{_mandir}/man3/File::MMagic.3pm

%check
make test TEST_VERBOSE=1

%files
%license COPYING
%doc README.en README.ja ChangeLog
%{perl_vendorlib}/File/MMagic.pm
%{_mandir}/man3/File::MMagic.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.30-1
- Package the fixed CPAN release with the original tests and notices.
