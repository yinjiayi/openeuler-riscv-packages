# SPDX-License-Identifier: Apache-2.0
Name:           libio-interactive-perl
Version:        1.027
Release:        1%{?dist}
Summary:        Handle terminal and non-terminal streams in Perl
License:        Artistic-2.0
URL:            https://metacpan.org/dist/IO-Interactive
Source0:        IO-Interactive-1.027.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.008
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 1
BuildRequires:  perl(version) >= 0.86
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  util-linux
Requires:       perl >= 5.008
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Handle terminal and non-terminal streams in Perl

%prep
%autosetup -n IO-Interactive-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/IO/Interactive.pm
test -f %{buildroot}%{_mandir}/man3/IO::Interactive.3pm

%check
make test TEST_VERBOSE=1
# The default harness is not a terminal. Run the unchanged originals in
# a genuine PTY too, and check TAP because interactive.t emits raw TAP.
/usr/bin/script -q -e -c 'test -t 0 && test -t 1 && exec %{__perl} -Mblib t/interactive.t' /dev/null </dev/null > interactive.pty.tap
/usr/bin/script -q -e -c 'test -t 0 && test -t 1 && exec %{__perl} -Mblib t/is_interactive.t' /dev/null </dev/null > is_interactive.pty.tap
%{__perl} - interactive.pty.tap is_interactive.pty.tap <<'PTYPERL'
use strict;
use warnings;

sub read_tap {
    my ($path) = @_;
    open my $fh, '<', $path or die "$path: $!";
    my @lines = <$fh>;
    close $fh or die "$path: $!";
    s/\r?\n\z// for @lines;
    print "PTY $path\n", map { "$_\n" } @lines;
    return @lines;
}

my @interactive = read_tap(shift @ARGV);
die "unexpected interactive.t PTY TAP"
    unless join("\n", @interactive) eq "1..2\nok 1\nok 2";

my @detection = read_tap(shift @ARGV);
die "unexpected is_interactive.t PTY plan" unless @detection == 10 && pop(@detection) eq '1..9';
for my $i (1 .. 2) {
    die "unexpected no-terminal assertion $i in PTY"
        unless $detection[$i - 1] eq "ok $i # skip connected to a terminal";
}
for my $i (3 .. 9) {
    die "terminal assertion $i did not run and pass"
        unless $detection[$i - 1] =~ /\Aok \Q$i\E(?: - [^#\r\n]+)?\z/;
}
print "Original real-PTY TAP verified: 9 passed, 2 intrinsic skips\n";
PTYPERL

%files
%license LICENSE
%doc README.pod Changes SECURITY.md
%{perl_vendorlib}/IO/Interactive.pm
%{_mandir}/man3/IO::Interactive.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.027-1
- Package the original release and verify default and real-terminal behavior.
