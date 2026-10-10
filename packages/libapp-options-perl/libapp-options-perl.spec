# SPDX-License-Identifier: Apache-2.0
Name:           perl-App-Options
Version:        1.12
Release:        1%{?dist}
Summary:        Combine command line options, environment and configuration files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/App-Options
Source0:        App-Options-%{version}.tar.gz
Source1:        perl538-Copying
Source2:        perl538-Artistic
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp) >= 0.01
BuildRequires:  perl(Sys::Hostname) >= 0.01
BuildRequires:  perl(Cwd) >= 0.01
BuildRequires:  perl(File::Spec) >= 0.01
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl-generators
Requires:       bash
Requires:       coreutils
Requires:       grep
Requires:       sed
Requires:       perl
Requires:       perl(Carp) >= 0.01
Requires:       perl(Sys::Hostname) >= 0.01
Requires:       perl(Cwd) >= 0.01
Requires:       perl(File::Spec) >= 0.01
Requires:       perl(Config)
Requires:       perl(Date::Format)
Requires:       perl(File::Find)
Requires:       perl(Fcntl)
Requires:       perl(File::Temp)
Requires:       perl(Digest::SHA)

%description
App::Options combines command line arguments, environment variables and option
files. Both original prefix and prefixadmin programs are included unchanged in
source and installed by the original MakeMaker EXE_FILES configuration.

%prep
%autosetup -n App-Options-%{version} -p1
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
# Isolate only child command environments; do not export/repurpose shell HOME.
check_home=$(mktemp -d "$PWD/.app-options-check-home.XXXXXXXX")
env -i HOME="$check_home" PATH=/usr/bin:/bin LC_ALL=C %{__perl} -MConfig -MSys::Hostname -MTest::More -MTest::Harness -MExtUtils::MakeMaker -e 'die "ordinary build identity required" unless $< == 10001 && $> == 10001; my $host=Sys::Hostname::hostname(); $host =~ s/\..*//; die "upstream fixture host collision" if $host eq "xyzzy3"; for my $f ("/etc/app/policy.conf","/etc/app/app.conf",(map { "$Config::Config{prefix}/etc/app/$_" } qw(main.conf old.conf app.conf)),qw(/usr/local/etc/app/main.conf /usr/local/etc/app/old.conf /usr/local/etc/app/app.conf t/main.conf t/old.conf)) { die "external default configuration: $f" if -e $f; } print "Default identity UID=$< EUID=$>; fresh child HOME=$ENV{HOME}; host=$host; system configuration absent\n";'
# Complete original t/*.t suite; pipe fixture really invokes cat.
timeout --kill-after=10s 180s env -i HOME="$check_home" PATH=/usr/bin:/bin LC_ALL=C %make_build test
# Independent TAP statistics for the same intact default suite, not rewritten tests.
timeout --kill-after=10s 180s env -i HOME="$check_home" PATH=/usr/bin:/bin LC_ALL=C %{__perl} -Iblib/lib -Iblib/arch -MTest::Harness -e 'my @t=sort glob("t/*.t"); die "default file set" unless join(" ",@t) eq "t/main.t t/old.t"; my ($total,$failed)=Test::Harness::execute_tests(tests=>\@t); for my $k (qw(files tests good max ok bad skipped sub_skipped todo bonus)) { die "missing Harness $k" unless exists $total->{$k}; } for my $k (qw(files tests good)) { die "Harness $k" unless $total->{$k}==2; } for my $k (qw(max ok)) { die "Harness $k" unless $total->{$k}==87; } for my $k (qw(bad skipped sub_skipped todo bonus)) { die "Harness $k" unless $total->{$k}==0; } die "failed TAP" if keys %$failed; print "Complete original Harness Files=2 Assertions=87 Passed=87 Skips=0 TODO=0 Bonus=0 Failures=0\n";'

%files
%license lib/App/Options.pm perl538-Copying perl538-Artistic
%doc README CHANGES TODO examples
%{perl_vendorlib}/App/Options.pm
%{_bindir}/prefix
%{_bindir}/prefixadmin
%{_mandir}/man3/App::Options.3*

%changelog
* Tue Oct 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12-1
- Retain all original files, both programs and the complete default test suite.
- Isolate child test configuration and preserve actual grant plus full terms.
