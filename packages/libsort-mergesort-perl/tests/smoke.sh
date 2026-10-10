#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- perl-Sort-MergeSort
rpm -q --whatprovides 'perl(Sort::MergeSort)'
rpm -q --whatprovides 'perl(Sort::MergeSort::Iterator)'
rpm -q --whatprovides 'perl(Test::NoWarnings)'

# Verify whole installed notices/modules, not just a synthesized grant excerpt.
expect_file() {
  local suffix=$1 expected=$2 file
  local -a matches=()
  while IFS= read -r file; do
    if [[ "$file" == */"$suffix" ]]; then matches+=("$file"); fi
  done < <(rpm -ql -- perl-Sort-MergeSort)
  [[ ${#matches[@]} -eq 1 ]]
  [[ -f "${matches[0]}" && ! -L "${matches[0]}" && ! -x "${matches[0]}" ]]
  echo "$expected  ${matches[0]}" | sha256sum -c -
}
expect_file Sort-MergeSort-main-original.txt e0edaf39c15477ca99a4bef9fb2eaaa920fa919be55af1393ec653648b94dc1e
expect_file Sort-MergeSort-Iterator-original.txt e26be8ab47e420b6b5770ba18ce9382b3604617a03d2b4195503c79324f29931
expect_file Artistic-2.0-full-original.md 3020f5d30b72430ef9a4346b0dcf8c7c57a96685f4e148e2108dcb50804692e7
expect_file LGPL-2.1-full-original.txt 20e50fe7aae3e56378ebf0417d9de904f55a0e61e4df315333e632a4d3555d95
expect_file Perl-Artistic-full-original.txt dd90d4f42e4dcadf5a7c09eea0189d93c7b37ae560c91f0f6d5233ed3b9292a2
expect_file Perl-Copying-full-original.txt d77d235e41d54594865151f4751e835c5a82322b0e87ace266567c3391a4b912
expect_file Object-Relation-Build-original.txt 34a818107140c7b621a5fd737a6587059a661bd289cdd3fb6a40edbc9873ebe3
expect_file Object-Relation-Iterator-original.txt 2022105dec955a04eeb0d300f406e9f1a592457f24cc8e67eff846e3274671b3
expect_file Sort/MergeSort.pm e0edaf39c15477ca99a4bef9fb2eaaa920fa919be55af1393ec653648b94dc1e
expect_file Sort/MergeSort/Iterator.pm e26be8ab47e420b6b5770ba18ce9382b3604617a03d2b4195503c79324f29931

perl -MSort::MergeSort=mergesort -MSort::MergeSort::Iterator -e '
  die "main version\n" unless $Sort::MergeSort::VERSION eq "0.31";
  die "iterator version\n" unless $Sort::MergeSort::Iterator::VERSION eq "0.01";
  my @a=(1,3,5); my @b=(2,4,6);
  my $left=Sort::MergeSort::Iterator->new(sub {shift @a});
  my $right=Sort::MergeSort::Iterator->new(sub {shift @b});
  my $merged=mergesort(sub {$_[0] <=> $_[1]},$left,$right);
  die "merged stream\n" unless join(",",$merged->all) eq "1,2,3,4,5,6";
  die "empty merge\n" if defined mergesort(sub {$_[0] <=> $_[1]})->next;
  my @v=(7,8); my $iter=Sort::MergeSort::Iterator->new(sub {shift @v});
  die "peek/position\n" unless $iter->peek==7 && $iter->position==0;
  die "next/current\n" unless $iter->next==7 && $iter->current==7;
  die "remaining/end\n" unless $iter->next==8 && !defined $iter->next;
'
