# SPDX-License-Identifier: Apache-2.0
Name:           perl-Regexp-Stringify
Version:        0.06
Release:        1%{?dist}
Summary:        Stringify Perl regular expression objects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Regexp-Stringify
Source0:        Regexp-Stringify-0.06.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Exporter)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl

%description
Stringify Perl regular expression objects

%prep
%autosetup -p1 -n Regexp-Stringify-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Regexp/Stringify.pm
%{_mandir}/man3/Regexp::Stringify.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package Regexp::Stringify with its original tests.
