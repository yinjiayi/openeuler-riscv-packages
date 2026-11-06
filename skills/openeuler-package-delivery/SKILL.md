---
name: openeuler-package-delivery
description: >-
  Coordinate sustained openEuler package delivery across existing PR acceptance, failed-PR repair
  and new-package intake. Use for a recurring delivery round or a parallel package expansion batch,
  not for a read-only review, one isolated recipe edit, or changing repository protections.
---

# Parallel Package Delivery

Deliver independently validated single-package PRs, repairs, qualified explicit merges and verified releases. Read the actual checkout's `AGENTS.md` and the current plan first; they own safety and acceptance policy. Consult relevant history by reference rather than loading the whole tracking log. This skill schedules work; it does not waive gates or authorize additional remote operations.

## Queues and ownership

Maintain three independent queues: **intake** contains unrepresented canonical candidates; **repair** contains actionable observed failures or evidence gaps; **merge-review** contains PRs selected for full acceptance, not already proven mergeable. CI waiting and external holds are states within the queues, not failures or extra delivery credit.

Use one `delivery-queue` SQLite database per repository for local worker assignment. A **dispatch lease** reserves a canonical package for one worker on this host; it does not replace `claim-repair`'s exact-head/remote-state lease, a CI result, or the merge gate. Workers on another host need separate reviewed coordination; copying the database does not provide distributed locking.

1. Check host resources, current checkout/main and user edits. Choose concurrency from available agent slots, memory/disk headroom, API limits and remote CI capacity. Reserve work for both actionable older PRs and independent intake; do not spend every slot waiting on one CI run or dependency chain. Each implementation worker owns a different package, checkout and output directory. The coordinator owns tracking updates and serial merge/publication decisions.
2. Collect one full, paginated, exact-head membership/file/CI snapshot for the round and share it:

```bash
python3 scripts/delivery-queue snapshot --repo "$github_repo" --repo-root . --workers 4 --output "$round_dir/snapshot.json"
python3 scripts/delivery-queue sync --db "$queue_db" --snapshot "$round_dir/snapshot.json" --candidates "$candidate_file"
```

The worker count above is a bounded read-concurrency example, not a fixed requirement or authorization for four target builds. `--candidates` takes a JSON array with one canonical `package_id` per entry and an optional `blocker`; it is an assignment list, not source/license admission evidence. Omit it when reconciling PRs only. Reconcile changing membership/heads; a failed or incomplete scan cannot establish whole-queue coverage. Current head/base and complete required CI are still re-read immediately before every merge. The CLI does not spawn agents or merge PRs; the coordinator must actually assign available workers.
3. Claim independent work atomically; select the appropriate `--queue`:

```bash
python3 scripts/delivery-queue claim --db "$queue_db" --repo "$github_repo" --queue intake --owner "$worker_id" --expected-main "$main_sha" --output "$worker_dir/claim.json"
```

An intake worker uses `openeuler-rpm-onboard`; a version-update worker uses `openeuler-rpm-update`; a repair worker uses `openeuler-riscv-repair` and obtains its additional exact-head repair lease. Use `linux-package-discovery` only when fresh catalog/lineage work is needed. Read only the skills required for the assigned operation.
4. Before source downloads, exclude canonical/open-PR/provider duplicates using current indexes. Inspect fixed official sources, licensing, dependencies and original tests for surviving candidates. A candidate hold records reason, next action and resume condition, then releases its worker to another package. Never loosen admission just to fill capacity.
5. After a verified PR submission or repair push, record its exact head and CI handoff, release the dispatch lease as `waiting`, and immediately claim the next independent package. Do not wait for the submitted package to merge. Continue until the authorized batch budget/cap, a genuine scoped blocker or the milestone stop condition; one successful PR is not the whole batch. The maximum 100 new single-package PRs per round is a ceiling, not a quota or a worker count.

```bash
python3 scripts/delivery-queue release --db "$queue_db" --repo "$github_repo" --owner "$worker_id" --lease-id "$lease_id" --outcome waiting --reason "Submitted exact head; target CI pending"
```

Use `blocked` with the precise recovery condition for an external hold, `requeue` for unfinished actionable work, and `complete` only for the assigned operation's observed outcome. Renew long-running leases; expiry never permits a stale push. New snapshots determine readiness after CI changes; do not repeatedly claim unchanged waiting work. A snapshot timestamp or unrelated main advance does not clear a manual hold. After verifying a specific recovery condition, the coordinator may explicitly restore scheduling eligibility:

```bash
python3 scripts/delivery-queue requeue --db "$queue_db" --repo "$github_repo" --owner "$coordinator_id" --expected-main "$main_sha" --item-key "$item_key" --reason "$verified_recovery"
```

Use `intake:PACKAGE_ID` or `pr:NUMBER` for the item key. Requeue does not remove remote blocking labels, clear a candidate blocker or reset the semantic repair budget; those still require their own applicable evidence and authority.
6. Review selected PRs concurrently, but merge only serially through the repository's full admission path after `github-credential-guard`. Keep Auto-merge disabled. The acceptance receipt must bind current main/head, required CI, official source, original tests, actual install and physical RPM/SRPM; green routing or infrastructure-only checks are insufficient. Read back each merge/new main before the next. Independently verify newly merged-main CI and immutable public metadata/bytes before crediting a release.
7. Persist delivery receipts outside temporary directories before recording durable success. Append compact counts, links, scoped holds and next milestone to the existing tracker; update current plan state once, not one competing narrative per worker. Report new PRs, repairs, qualified merges and verified publications separately; one package passing several stages is not several newly onboarded packages.

## Batch acceptance

Retain whole-queue coverage and actual delivery counts, plus oldest actionable age, active/waiting/blocked work and concrete resume conditions. Unchanged scans are not delivery; a read-only audit remains a valid audit, not a delivery batch. If all queues are externally blocked, explain each affected scope rather than inventing a fix or repeatedly requesting the same decision.
