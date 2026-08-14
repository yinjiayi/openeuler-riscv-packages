#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

repo_root=/opt/openeuler-riscv-rpm-repo
upload_home=/var/lib/openeuler-rpmrepo-upload
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
public_key=${1:-"$source_dir/deploy-key.pub"}

[[ $EUID -eq 0 ]] || { printf 'install.sh must run as root\n' >&2; exit 1; }
[[ -f $public_key ]] || { printf 'deploy public key is missing: %s\n' "$public_key" >&2; exit 1; }
command -v apt-get >/dev/null || { printf 'this installer requires apt-get\n' >&2; exit 1; }
missing_dependencies=false
for command in createrepo_c nginx rpm rsync /usr/bin/rrsync; do
  if ! command -v "$command" >/dev/null; then
    missing_dependencies=true
  fi
done
if [[ $missing_dependencies = true ]]; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y --no-install-recommends nginx createrepo-c rpm rsync openssh-server
fi
for command in createrepo_c nginx rpm rsync /usr/bin/rrsync; do
  command -v "$command" >/dev/null || { printf 'required command is missing: %s\n' "$command" >&2; exit 1; }
done

key_type=$(awk 'NR == 1 {print $1}' "$public_key")
key_value=$(awk 'NR == 1 {print $2}' "$public_key")
line_count=$(awk 'NF {count++} END {print count+0}' "$public_key")
[[ $key_type = ssh-ed25519 && $key_value =~ ^[A-Za-z0-9+/]+={0,2}$ && $line_count -eq 1 ]] || {
  printf 'deploy public key must contain exactly one ssh-ed25519 key\n' >&2
  exit 1
}

if ! id reposync >/dev/null 2>&1; then
  useradd --create-home --home-dir "$upload_home" --shell /bin/bash --user-group reposync
fi
usermod --lock reposync

install -d -o reposync -g reposync -m 0750 "$repo_root/incoming"
install -d -o root -g root -m 0700 "$repo_root/failed" "$repo_root/tmp"
install -d -o root -g www-data -m 0755 "$repo_root/public" "$repo_root/public/generations"
install -d -o root -g www-data -m 0755 "$repo_root/public/riscv64/Packages" "$repo_root/public/source/Packages"
install -d -o reposync -g reposync -m 0700 "$upload_home/.ssh"

authorized_key=$(mktemp "$upload_home/.ssh/.authorized_keys.XXXXXX")
trap 'rm -f -- "$authorized_key"' EXIT
printf 'restrict,command="/usr/bin/rrsync -wo -no-del -no-overwrite %s" %s %s\n' \
  "$repo_root/incoming" "$key_type" "$key_value" >"$authorized_key"
chown reposync:reposync "$authorized_key"
chmod 0600 "$authorized_key"
mv -f -- "$authorized_key" "$upload_home/.ssh/authorized_keys"
trap - EXIT

install -o root -g root -m 0755 "$source_dir/rpmrepo_publish.py" /usr/local/sbin/openeuler-rpmrepo-publish
install -o root -g root -m 0644 "$source_dir/openeuler-rpmrepo.default" /etc/default/openeuler-rpmrepo
install -o root -g root -m 0644 "$source_dir/openeuler-rpmrepo.service" /etc/systemd/system/openeuler-rpmrepo.service
install -o root -g root -m 0644 "$source_dir/openeuler-rpmrepo.path" /etc/systemd/system/openeuler-rpmrepo.path
install -o root -g root -m 0644 "$source_dir/openeuler-rpmrepo.timer" /etc/systemd/system/openeuler-rpmrepo.timer
install -o root -g root -m 0644 "$source_dir/nginx.conf" /etc/nginx/sites-available/openeuler-rpmrepo
rm -f /etc/nginx/sites-enabled/default
ln -sfn /etc/nginx/sites-available/openeuler-rpmrepo /etc/nginx/sites-enabled/openeuler-rpmrepo

/usr/local/sbin/openeuler-rpmrepo-publish --bootstrap
nginx -t
systemctl daemon-reload
systemctl enable --now openeuler-rpmrepo.path openeuler-rpmrepo.timer nginx
systemctl restart nginx

printf 'RPM repository installed. State: %s/public/state.json\n' "$repo_root"
