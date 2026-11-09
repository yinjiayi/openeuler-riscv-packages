<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxml-xpathengine-perl

This directory packages upstream `https://metacpan.org/dist/XML-XPathEngine` version `0.14` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The fixed PAUSE-signed CPAN archive is byte-identical to the Debian stable
0.14-2 original. The package retains Michel Rodriguez's original grant,
both complete Perl license texts, and the separate AxKit.com/Matt Sergeant
notice for the modified XML::XPath code.

All original tests run unchanged, including the POD and POD coverage tests.
The installed smoke verifies the child axis and a positional predicate on
a small in-memory node tree without relying on the source fixtures.
