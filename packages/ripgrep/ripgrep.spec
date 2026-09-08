# SPDX-License-Identifier: Apache-2.0
Name:           ripgrep
Version:        15.2.0
Release:        1%{?dist}
Summary:        A search tool that combines the usability of ag with the raw speed of grep
License:        MIT OR Unlicense
URL:            https://github.com/BurntSushi/ripgrep
Source0:        ripgrep-15.2.0.tar.gz
BuildRequires:  cargo
BuildRequires:  gcc


%description
ripgrep is a line-oriented search tool that recursively searches the current
directory for a regex pattern while respecting gitignore rules. It provides
Unicode-aware search, automatic filtering, and parallel directory traversal.

%prep
%autosetup -p1

%build
cargo build --release --locked

%install
install -D -m 0755 target/release/rg %{buildroot}%{_bindir}/rg
install -D -m 0644 COPYING %{buildroot}%{_datadir}/licenses/%{name}/COPYING
install -m 0644 LICENSE-MIT %{buildroot}%{_datadir}/licenses/%{name}/LICENSE-MIT
install -m 0644 UNLICENSE %{buildroot}%{_datadir}/licenses/%{name}/UNLICENSE
install -D -m 0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -m 0644 CHANGELOG.md %{buildroot}%{_docdir}/%{name}/CHANGELOG.md
install -m 0644 FAQ.md %{buildroot}%{_docdir}/%{name}/FAQ.md
install -m 0644 GUIDE.md %{buildroot}%{_docdir}/%{name}/GUIDE.md
target/release/rg --generate man > rg.1
target/release/rg --generate complete-bash > rg.bash
target/release/rg --generate complete-fish > rg.fish
target/release/rg --generate complete-zsh > _rg
install -D -m 0644 rg.1 %{buildroot}%{_mandir}/man1/rg.1
install -D -m 0644 rg.bash %{buildroot}%{_datadir}/bash-completion/completions/rg
install -D -m 0644 rg.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/rg.fish
install -D -m 0644 _rg %{buildroot}%{_datadir}/zsh/site-functions/_rg

%check
cargo test --all --locked
./target/release/rg --version | grep -F 'ripgrep %{version}'

%files
%license %{_datadir}/licenses/%{name}/COPYING
%license %{_datadir}/licenses/%{name}/LICENSE-MIT
%license %{_datadir}/licenses/%{name}/UNLICENSE
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/CHANGELOG.md
%doc %{_docdir}/%{name}/FAQ.md
%doc %{_docdir}/%{name}/GUIDE.md
%{_bindir}/rg
%{_mandir}/man1/rg.1*
%{_datadir}/bash-completion/completions/rg
%{_datadir}/fish/vendor_completions.d/rg.fish
%{_datadir}/zsh/site-functions/_rg

%changelog
* Fri Aug 21 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 15.2.0-1
- Initial openEuler RISC-V package with the complete upstream Cargo test suite.
