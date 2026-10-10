<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-Sort-MergeSort

This directory packages upstream `https://metacpan.org/release/Sort-MergeSort` version `0.31` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

A verified source is the exact official CPAN 0.31 archive whose SHA-256
`ad25e7c8d9a9ac8417d6de96c764ced9f477108490dfb960ae02a3db0a9c6efe`
matches its authorized/latest released API record and author `CHECKSUMS`.
The frozen Fedora Everything-source `perl-Sort-MergeSort` 0.31-31.fc44 row
at discovery `/rejections/169062` is identity/lineage evidence, not a license
grant or executable recipe. No shared registry or frozen snapshot is changed.

License scope is the per-component grant, not a blanket choice for this tree.
The original main module names David Sharnoff and Google and grants Artistic
2.0 OR LGPL 2.1. The original nested Iterator names David Wheeler/Kineticode
and grants Perl's terms. Its adapted iterator test shares a substantial body
with the original Object-Relation test; that original distribution declares
`license => 'perl'`, lists the test and retains the original Iterator grant.
The package preserves the scoped Perl branch and notices, without claiming
exact intermediate provenance or legal clearance. The combined expression is
`(Artistic-2.0 OR LGPL-2.1-only) AND (GPL-1.0-or-later OR Artistic-1.0-Perl)`.
The distribution's generated `license: unknown` and Fedora's legacy LGPLv2
label do not override the actual module grants.

Eight unmodified whole notice/term files are installed as non-executable
`%license` documents: current main/Iterator sources, fixed historical origin
Build.PL/Iterator sources, complete Artistic2/LGPL2.1 and Perl Artistic/Copying
terms. Supplement URL/digests are declared in `sources.yaml`. Historical
Object-Relation-v0.1.0 archive bytes match its official API, but the current
author CHECKSUMS has no backpan stanza. The separately fixed whole notice
endpoints match those bytes; that missing historical checksum remains a
research-channel limitation. Neither historical Build.PL nor Iterator is
executed/imported as a build input or dependency. The original source text
and all copyright/grant paragraphs remain byte-for-byte unchanged.

All 9 original files were inspected; both substantive default `t/*.t` files
are retained. Iterator tests constructor errors, position, peek/current/next,
all/do and destruction (44 planned assertions including Test::NoWarnings).
Merge tests retain 24 input streams, array-size recursion and D2/D3 data,
order/count/final completion checks. `%check` executes the unfiltered upstream
MakeMaker suite in CI. `Test::NoWarnings` remains a declared runtime dependency,
not merely a build prerequisite. Official SP3 RVA23 checksum-bound primary
metadata provides MakeMaker, Harness, Test::More, Test::NoWarnings, podlators
and other build tools, but lacks candidate RPM aliases and both module
Provides. This is metadata coverage, not installed-runtime evidence.

The installed smoke checks both module versions/Provides, merged values,
empty streams, iterator methods and exact hashes of all eight installed
notice documents plus both installed modules. No local upstream execution,
target build/install or success claim is made. Exact-head hosted CI must
establish the full suite, RPM/SRPM and installed smoke; pull requests publish
no repository packages. No RISC-V patch or native-only behavior is required.
