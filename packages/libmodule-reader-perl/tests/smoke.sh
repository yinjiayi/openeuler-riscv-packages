#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-module-reader
perl -MModule::Reader=module_content,module_handle - <<'PERL'
    die "unexpected module version\n" unless $Module::Reader::VERSION == 0.003003;
    my $source = module_content("Module::Reader");
    my $handle = module_handle("Module::Reader");
    local $/;
    die "module source did not round trip\n"
        unless $source =~ /^package Module::Reader;/m && <$handle> eq $source;
    print "installed module source and handle agree\n";

    {
        package ReaderSmoke::FalseCan;
        sub can { die "overridden can must not be called\n" }
        sub ReaderSmoke::FalseCan::INC { open my $fh, "<", \"from INC" or die $!; return $fh }
    }
    {
        package ReaderSmoke::Auto;
        our $AUTOLOAD;
        sub AUTOLOAD {
            die "unexpected AUTOLOAD: $AUTOLOAD\n" unless $AUTOLOAD =~ /::INC\z/;
            open my $fh, "<", \"from AUTOLOAD" or die $!;
            return $fh;
        }
        sub DESTROY {}
    }
    {
        package ReaderSmoke::Throws;
        sub ReaderSmoke::Throws::INC { die "existing hook exception\n" }
    }
    {
        package ReaderSmoke::Stringy;
        use overload q{""} => "as_string";
        sub can { die "overridden can on overload must not be called\n" }
        sub as_string { die "string overload must not be called\n" }
    }
    die "real INC dispatch changed\n"
        unless module_content("ReaderSmokeFixture", bless({}, "ReaderSmoke::FalseCan")) eq "from INC";
    die "AUTOLOAD dispatch changed\n"
        unless module_content("ReaderSmokeFixture", bless({}, "ReaderSmoke::Auto")) eq "from AUTOLOAD";
    eval { module_content("ReaderSmokeFixture", bless({}, "ReaderSmoke::Throws")) };
    die "real hook exception was changed: $@" unless $@ eq "existing hook exception\n";
    eval { module_content("ReaderSmokeFixture", bless({}, "ReaderSmoke::Stringy")) };
    die "string overload dispatch changed: $@"
        unless $@ =~ /object method "INC" via package "ReaderSmoke::Stringy"/;

    if ($^V >= v5.37.8) {
        eval { module_content("ReaderSmokeFixture", bless({}, "ReaderSmoke::Unsupported")) };
        die "unexpected unsupported-object diagnostic: $@"
            unless $@ =~ /"INC", nor "INCDIR" nor string overload via package "ReaderSmoke::Unsupported" in object hook in \@INC/;
    }
    print "installed object hook behavior preserved\n";
PERL
