# Discovery snapshots

Each discovery run writes one immutable JSON snapshot here. A snapshot records the actual resolved distribution release/codename, enabled official components, observation time, source URLs, metadata SHA-256 values, normalization lineage, exclusions, and deduplication decisions. Do not replace a historical snapshot when a rolling or stable alias moves.

The snapshot also records the policy that produced its decisions. New runs require a verified release source—an HTTPS official stable release/tag archive pinned by its full SHA-256—before a component is `eligible`. Historical snapshots remain immutable and may predate that fail-closed rule; consumers must honor the policy embedded in each snapshot and re-resolve old candidates before onboarding.
