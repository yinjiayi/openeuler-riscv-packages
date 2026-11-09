#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libyaml-appconfig-perl
PERL_USE_UNSAFE_INC=0 perl -MYAML::AppConfig -e '
    die "version" unless YAML::AppConfig->VERSION eq "0.19";
    my $config = YAML::AppConfig->new(
        yaml_class => "YAML",
        string => qq{---\nbase: riscv\nmessage: "\$base-ready"\n},
    );
    die "interpolation" unless $config->get("message") eq "riscv-ready";
    $config->set("base", "rva23");
    my $roundtrip = YAML::AppConfig->new(yaml_class => "YAML", string => $config->dump);
    die "roundtrip" unless $roundtrip->get("message") eq "rva23-ready";
    print "installed YAML interpolation and roundtrip passed\n";
'
