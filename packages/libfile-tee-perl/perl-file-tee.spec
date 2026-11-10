# SPDX-License-Identifier: Apache-2.0
Name:           perl-file-tee
Version:        0.07
Release:        1%{?dist}
Summary:        Replicate output written to a Perl stream
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Tee
Source0:        File-Tee-0.07.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(Fcntl)
Requires:       perl(POSIX)
Requires:       perl(Symbol)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Replicate output written to a Perl stream

%prep
%autosetup -n File-Tee-%{version}
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
%{perl_vendorlib}/File/Tee.pm
%{_mandir}/man3/File::Tee.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package the fixed upstream release with its original default tests.
