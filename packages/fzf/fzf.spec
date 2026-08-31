# SPDX-License-Identifier: Apache-2.0
Name:           fzf
Version:        0.74.3
Release:        1%{?dist}
%global debug_package %{nil}
Summary:        Command-line fuzzy finder
License:        MIT
URL:            https://github.com/junegunn/fzf
Source0:        fzf-0.74.3.tar.gz
BuildRequires:  golang
BuildRequires:  make


%description
fzf is an interactive command-line filter that uses fuzzy matching to select
items from any list. This package also installs the upstream tmux helper,
manual pages, shell integration, and Vim plugin.

%prep
%autosetup -p1

%build
%set_build_flags
go build -buildvcs=false -trimpath \
  -ldflags "-s -w -X main.version=%{version} -X main.revision=source" \
  -o fzf .

%install
install -Dpm0755 fzf %{buildroot}%{_bindir}/fzf
install -Dpm0755 bin/fzf-tmux %{buildroot}%{_bindir}/fzf-tmux
install -Dpm0755 bin/fzf-preview.sh %{buildroot}%{_datadir}/fzf/bin/fzf-preview.sh
install -Dpm0644 man/man1/fzf.1 %{buildroot}%{_mandir}/man1/fzf.1
install -Dpm0644 man/man1/fzf-tmux.1 %{buildroot}%{_mandir}/man1/fzf-tmux.1
install -Dpm0644 shell/completion.bash \
  %{buildroot}%{_datadir}/bash-completion/completions/fzf
install -Dpm0644 shell/completion.zsh \
  %{buildroot}%{_datadir}/zsh/site-functions/_fzf
install -Dpm0644 shell/completion.fish \
  %{buildroot}%{_datadir}/fzf/shell/completion.fish
install -Dpm0644 shell/key-bindings.bash \
  %{buildroot}%{_datadir}/fzf/shell/key-bindings.bash
install -Dpm0644 shell/key-bindings.zsh \
  %{buildroot}%{_datadir}/fzf/shell/key-bindings.zsh
install -Dpm0644 shell/key-bindings.fish \
  %{buildroot}%{_datadir}/fzf/shell/key-bindings.fish
install -Dpm0644 plugin/fzf.vim \
  %{buildroot}%{_datadir}/vim/vimfiles/plugin/fzf.vim

%check
FZF_VERSION=%{version} FZF_REVISION=source %make_build test
./fzf --version | grep -F '%{version} (source)'

%files
%license LICENSE src/LICENSE
%doc README.md ADVANCED.md BUILD.md CHANGELOG.md
%{_bindir}/fzf
%{_bindir}/fzf-tmux
%{_datadir}/fzf/
%{_datadir}/bash-completion/completions/fzf
%{_datadir}/zsh/site-functions/_fzf
%{_datadir}/vim/vimfiles/plugin/fzf.vim
%{_mandir}/man1/fzf.1*
%{_mandir}/man1/fzf-tmux.1*

%changelog
* Fri Aug 21 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.74.3-1
- Package the upstream stable release with Go unit tests and shell integration.
