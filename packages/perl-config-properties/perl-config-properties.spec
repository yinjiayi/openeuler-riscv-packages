# SPDX-License-Identifier: Apache-2.0
Name:           perl-config-properties
Version:        1.80
Release:        1%{?dist}
Summary:        Read and write Java-style properties files in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Config-Properties
Source0:        https://cpan.metacpan.org/authors/id/S/SA/SALVA/Config-Properties-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Text::Wrap) >= 2001.0929
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(PerlIO)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Encode)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Text::Wrap) >= 2001.0929
Requires:       perl(File::Temp)
Requires:       perl(IO::Handle)
Requires:       perl(PerlIO)
Requires:       perl(Errno)

%description
Config::Properties reads and writes Java-style properties files. It
supports comments, escaping, validation, and ordering for saved keys.

%prep
%setup -q -n Config-Properties-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Config/Properties.pm
%{_mandir}/man3/Config::Properties.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.80-1
- Package the fixed upstream release and retain the complete default tests.
