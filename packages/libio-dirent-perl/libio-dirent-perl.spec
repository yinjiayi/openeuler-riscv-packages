# SPDX-License-Identifier: Apache-2.0
Name:           libio-dirent-perl
Version:        0.05
Release:        1%{?dist}
Summary:        Read directory entries and file types from Perl using XS
License:        Artistic-1.0-Perl
URL:            https://metacpan.org/dist/IO-Dirent
Source0:        IO-Dirent-0.05.tar.gz
Source1:        Artistic-1.0-Perl.txt
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::ParseXS)
BuildRequires:  perl(Config)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test)
BuildRequires:  perl(blib)
Requires:       perl
Requires:       perl(DynaLoader)
Requires:       perl(Exporter)

%description
Read directory entries and file types from Perl using XS

%prep
%autosetup -n IO-Dirent-%{version} -p1
cp -p %{SOURCE1} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorarch}/IO/Dirent.pm
test -f %{buildroot}%{perl_vendorarch}/auto/IO/Dirent/Dirent.so
test -f %{buildroot}%{_mandir}/man3/IO::Dirent.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt
%doc Changes
%{perl_vendorarch}/IO/Dirent.pm
%dir %{perl_vendorarch}/auto/IO/Dirent
%{perl_vendorarch}/auto/IO/Dirent/Dirent.so
%{_mandir}/man3/IO::Dirent.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package verified source, original XS tests and Perl Artistic notices.
