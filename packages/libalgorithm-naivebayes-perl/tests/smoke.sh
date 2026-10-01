#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- perl-Algorithm-NaiveBayes
perl -MAlgorithm::NaiveBayes -e '
  die "unexpected version\n"
    unless $Algorithm::NaiveBayes::VERSION eq "0.04";
  my $model = Algorithm::NaiveBayes->new;
  $model->add_instance(attributes => { sheep => 1 }, label => "farming");
  $model->add_instance(attributes => { fang => 1 }, label => "vampire");
  $model->train;
  my $prediction = $model->predict(attributes => { sheep => 1 });
  die "Bayesian category prediction failed\n"
    unless $prediction->{farming} > $prediction->{vampire};
  my $discrete = Algorithm::NaiveBayes->new(model_type => "Discrete");
  die "discrete model missing\n"
    unless $discrete->isa("Algorithm::NaiveBayes::Model::Discrete");
'
