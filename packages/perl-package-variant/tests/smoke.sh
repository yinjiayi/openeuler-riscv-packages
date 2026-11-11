#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-package-variant
perl -MPackage::Variant -e '
  die "unexpected version" unless $Package::Variant::VERSION == 1.003002;
  {
    package PackageVariantSmoke;
    Package::Variant->import;
    sub make_variant {
      my ($self, $target, $label) = @_;
      install("label", sub { $label });
    }
  }
  my $a = PackageVariantSmoke->build_variant("alpha");
  my $b = PackageVariantSmoke->build_variant("beta");
  die "wrong variant names" unless $a ne $b;
  die "wrong variant behavior" unless $a->label eq "alpha" && $b->label eq "beta";
'
