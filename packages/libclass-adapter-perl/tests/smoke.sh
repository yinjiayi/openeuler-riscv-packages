#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Class-Adapter
rpm -q --whatprovides 'perl(Class::Adapter)'
rpm -q --whatprovides 'perl(Class::Adapter::Builder)'
rpm -q --whatprovides 'perl(Class::Adapter::Clear)'
perl -MClass::Adapter -MClass::Adapter::Builder -MClass::Adapter::Clear -e '
  die "wrong installed version\n" unless $Class::Adapter::VERSION eq "1.09";
  { package Smoke::Target; sub new { bless {}, shift } sub ping { "pong" } }
  my $target = Smoke::Target->new;
  my $adapter = Class::Adapter->new($target);
  die "underlying object lost\n" unless $adapter->_OBJECT_ == $target;
  my $clear = Class::Adapter::Clear->new($target);
  die "delegation failed\n" unless $clear->ping eq "pong";
  my $builder = Class::Adapter::Builder->new("Smoke::Generated");
  die "Builder ISA setup failed\n" unless $builder->set_ISA("_OBJECT_");
  die "Builder AUTOLOAD setup failed\n" unless $builder->set_AUTOLOAD(1);
  die "Builder output missing\n" unless $builder->make_class =~ /package Smoke::Generated;/;
'
