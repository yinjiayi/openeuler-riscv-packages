<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-autoformat-perl

The frozen Ubuntu discovery row maps this component to official CPAN
[Text-Autoformat 1.75](https://metacpan.org/dist/Text-Autoformat).
The upstream archive and publisher CHECKSUMS agree on SHA-256
`9dd4f4ce3daec4b4dbf5b59dac4568a8946aed12c28b4e5988c8e8c602c6b771`.
Its LICENSE grants the Perl 5 license alternatives. The archive contains
only ordinary files and directories under one top-level tree.

The current official RVA23 and verified supplemental repository primary
and filelists metadata contain no Text::Autoformat provider or module path.
The supplemental generation from Text::Reform supplies its required
`perl(Text::Reform)`; official metadata supplies `perl(Text::Tabs)`.
These checks describe that repository snapshot, not future repositories.

The SPEC retains the upstream default five test files. Installed smoke
checks the RPM provider, version and empty-input behavior. The local recipe
checks do not establish target build, installation or publication: those
remain subject to exact-head CI and independent artifact verification.
