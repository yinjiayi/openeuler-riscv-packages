#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

oe_load_policy
[[ $OE_POLICY_ENROLLMENT_ENABLED == true ]] || oe_die 'runner policy is not enabled'
[[ ${GITHUB_REPOSITORY-} == "$OE_POLICY_REPOSITORY" ]] || oe_die 'job repository is not allowed'
[[ ${GITHUB_REF-} == "$OE_POLICY_REF" ]] || oe_die 'only the protected main ref is allowed'
[[ ${GITHUB_SHA-} =~ ^[0-9a-f]{40}$ ]] || oe_die 'job SHA is missing or invalid'

case ",$OE_POLICY_WORKFLOW_REFS," in
  *,"${GITHUB_WORKFLOW_REF-}",*) ;;
  *) oe_die 'workflow is not one of the two root-approved workflows on main' ;;
esac

case ",$OE_POLICY_EVENTS," in
  *,"${GITHUB_EVENT_NAME-}",*) ;;
  *) oe_die 'workflow event is not allowed' ;;
esac

# pull_request and pull_request_target are intentionally absent from the
# allow-list. A called workflow retains the caller event/ref, so an external
# fork cannot cross this gate merely by naming the runner label.
case ${GITHUB_EVENT_NAME-} in
  pull_request|pull_request_target|merge_group|workflow_run)
    oe_die 'untrusted or indirect events cannot run on this persistent public-repository runner'
    ;;
esac

printf 'Trusted protected-main job policy passed.\n'
