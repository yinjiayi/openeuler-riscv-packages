# SPDX-License-Identifier: Apache-2.0
Name:           perl-App-Control
Version:        1.07
Release:        1%{?dist}
Summary:        Apachectl-style control of a script or executable in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/App-Control
Source0:        App-Control-%{version}.tar.gz
Source1:        perl538-Copying
Source2:        perl538-Artistic

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(sigtrap)
BuildRequires:  perl-generators
Requires:       coreutils
Requires:       grep
Requires:       perl
Requires:       perl(Digest::SHA)
Requires:       perl(File::Basename)
Requires:       perl(File::Path)
Requires:       perl(File::Temp)

%description
App::Control provides object methods for apachectl-style start, stop,
restart, status and HUP control of a caller-specified executable and pidfile.
The original program and complete original default tests are retained.

%prep
%autosetup -n App-Control-%{version} -p1
cp -p %{SOURCE1} perl538-Copying
cp -p %{SOURCE2} perl538-Artistic

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Fresh source/build directory in the disposable CI PID namespace; no host PID use.
%{__perl} -MExtUtils::MakeMaker -MTest::Harness -MFile::Basename -MFile::Path -e 'require sigtrap; die "root test identity" unless $< == 10001 && $> == 10001; print "Default test identity UID=$< EUID=$> GID=$( EGID=$)\n"; die "stale default fixture" if -e "pids/test.pid" || -e "ignore.tmp"; die "original helper mode" unless -x "sample/test.pl"; print "Original default test/helper prerequisites verified\n";'
# GNU timeout owns a process group, including unchanged fork/exec helper children.
# Never use --foreground or reuse pids/test.pid; MakeMaker Harness parses not-ok.
timeout --kill-after=10s 180s %make_build test

%files
%license README perl538-Copying perl538-Artistic
%doc Changes
%{perl_vendorlib}/App/Control.pm
%{_mandir}/man3/App::Control.3*

%changelog
* Tue Oct 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Preserve official source, both complete default assertions and original notices.
- Bound the unchanged child-process suite; keep installed smoke constructor-only.
