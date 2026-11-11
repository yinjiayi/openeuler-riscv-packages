<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdali 1.8.1

EarthScope's C client library for the DataLink protocol is not a server. The
genuine frozen AUR libdali 1.8-3 row points to IRIS/libdali, which officially
redirects to EarthScope/libdali. The latest formal non-prerelease is v1.8.1
(2023-12-01), fixed commit `89363cacea767537b011722302c8c08e22bc04ba`.
Its official tag archive SHA-256 is
`367f847b145a8dd5b3918167ceb9f999849e6abba128ece7caf4440b745eb62e`.
All 37 ordinary archive files match the complete exact Git tree's blob bytes.
The lightweight tag and commit are unsigned; independent signature verification
is not claimed. Frozen lineage is not a current complete catalog scan.

Original `all: static` remains unchanged. The shared library is additionally
built because original `install: shared` installs it, the header, dali.pc and
complete example source directory. The original default-built static archive is
explicitly installed. Documentation generation/push is a manual script, not a
default all/install dependency; it is not executed. No original source changes.

Both the complete Git tree and source archive lack a test directory. The stale
original test/check target invokes that absent directory: zero original runtime
cases are available. This package preserves the target unchanged and does not
claim upstream make check passed. Six added strict cases cover Gregorian leap
and calendar errors, epoch formatting (including negative epochs), ISO/SEED
parsing, stream identifiers, owned strings, and zero-payload reply headers.
The reply test never receives data or opens a socket. Assertions remain enabled.
Build and installed tests run the same driver; installed verification checks six
exact caller/symbol/target bindings using file identity, not loader path spelling.
Raw loader trace, SHA-256 and failing exit status are preserved. This does not
validate remote-server integration, security, privileged operation, performance,
native timing or broad network interoperability.

License: Apache-2.0 AND MIT. Original project files retain the root Apache2 grant.
gmtime64.c has Michael G Schwern's complete 2007-2010 MIT grant and derivation
attribution; its paired header references that implementation license. The
original footer contains the same-owner EarthScope logo and attributed
GitHub-corners SVG. All 37 original files are copied unchanged as notices before
the driver is generated, including embedded logo bytes. A full GitHub-corners
MIT notice is added as the 38th notice. Both build and installed tests verify
the complete notice checksum manifest. No independent trademark-use permission
or license for unbundled external URLs is claimed.

The auxiliary notice is official tholman/github-corners license.md, Git blob
`c7bf0888a0c3baad05323e57c524bc5fdbeb22b3`, SHA-256
`4153a48fc08e54790573416669164be803f7eb18b8d2d5b6233bf4c222951f06`.
It is copied below and into the SPEC notice, not mislabeled as a release or test
dependency in sources.yaml:

> The MIT License (MIT)
>
> Copyright (c) 2025 Tim Holman
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

The new driver has its own full MIT grant. Its installed executable/source
manifest is generated in check after RPM install-post stripping. The recipe
requires no undeclared fetch; actual trusted CI can have network access, so this
does not claim isolation. Local work is inert review and trusted repository
validation, not upstream compilation/execution, RPM or QEMU. Actual target CI,
RPM/SRPM products and complete supplemental namespace acceptance are still
required before merge/publication. Official closure is not a DNF SAT proof.
