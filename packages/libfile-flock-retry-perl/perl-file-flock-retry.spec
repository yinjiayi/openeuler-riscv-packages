# SPDX-License-Identifier: Apache-2.0
Name:           perl-file-flock-retry
Version:        0.632
Release:        1%{?dist}
Summary:        File locking with bounded retries for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Flock-Retry
Source0:        File-Flock-Retry-0.632.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.10.1
BuildRequires:  perl-generators
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Slurper)
BuildRequires:  perl(File::chdir)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(File::Temp) >= 0.2307
BuildRequires:  perl(IO::Handle)
Requires:       perl >= 5.10.1
Requires:       perl(Fcntl)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
File locking with bounded retries for Perl

%prep
%autosetup -n File-Flock-Retry-%{version} -p1
cat > TEMPLATE-NOTICES <<'NOTICE'
Dist::Zilla 6.017 generated portions: Copyright 2020 Ricardo SIGNES.
Dist::Zilla::Plugin::Test::Compile 2.058 generated portions:
Copyright 2009 Jérôme Quelin; authors Jérôme Quelin and Karen Etheridge.
Dist::Zilla::Plugin::Test::Perl::Critic::Subset 3.001.005 generated portions:
Copyright 2020, 2019 perlancar@cpan.org.
The reviewed generator portions are redistributable under the same
terms as Perl itself. The complete GPL and Artistic terms are retained
in the original distribution LICENSE.
NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE TEMPLATE-NOTICES
%doc README Changes
%{perl_vendorlib}/File/Flock/Retry.pm
%{_mandir}/man3/File::Flock::Retry.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.632-1
- Package the pinned release with its unchanged default suite.
