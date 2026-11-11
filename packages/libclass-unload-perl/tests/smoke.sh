#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-class-unload
perl -T -MClass::Unload -MClass::Inspector -e '
    package Smoke::ClassUnload;
    sub marker { 1 }
    package Smoke::ClassUnload::Nested;
    sub nested_marker { 2 }
    package main;
    $INC{"Smoke/ClassUnload.pm"} = __FILE__;
    die "fixture not loaded" unless Class::Inspector->loaded("Smoke::ClassUnload");
    die "unload failed" unless Class::Unload->unload("Smoke::ClassUnload");
    die "stale module entry" if exists $INC{"Smoke/ClassUnload.pm"};
    die "stale symbol" if Smoke::ClassUnload->can("marker");
    die "nested symbol lost" unless Smoke::ClassUnload::Nested->nested_marker == 2;
    print "installed Class::Unload removes class and load entry while preserving nested namespaces\n";
'
