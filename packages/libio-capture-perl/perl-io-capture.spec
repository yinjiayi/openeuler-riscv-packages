# SPDX-License-Identifier: Apache-2.0
Name:           perl-io-capture
Version:        0.05
Release:        1%{?dist}
Summary:        Capture Perl standard output and error streams
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/IO-Capture
Source0:        IO-Capture-0.05.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  sed
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
IO::Capture provides a base class and concrete implementations to capture
Perl standard output and error separately in the current process.

%prep
%autosetup -n IO-Capture-%{version}
for notice in lib/IO/Capture.pm lib/IO/Capture/Overview.pod lib/IO/Capture/Stderr.pm lib/IO/Capture/Stdout.pm; do
    printf 'Original notice from %%s\n\n' "$notice"
    sed -n '/^=head1 COPYRIGHT$/,/^=cut/p' "$notice"
    printf '\n'
done > IO-Capture-LICENSES

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license IO-Capture-LICENSES
%doc README Changes BUGS
%{perl_vendorlib}/IO/Capture.pm
%{perl_vendorlib}/IO/Capture/
%{_mandir}/man3/IO::Capture.3*
%{_mandir}/man3/IO::Capture::Overview.3*
%{_mandir}/man3/IO::Capture::Stderr.3*
%{_mandir}/man3/IO::Capture::Stdout.3*
%{_mandir}/man3/IO::Capture::Tie_STDx.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package the exact signed IO::Capture 0.05 release with its original tests and notices.
