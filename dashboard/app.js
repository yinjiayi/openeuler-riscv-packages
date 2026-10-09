// SPDX-License-Identifier: Apache-2.0
'use strict';

const stateOrder = ['published', 'build-succeeded', 'passed', 'managed', 'reviewed', 'open-pr', 'pr-open', 'ci-queued', 'building', 'repair-queued', 'codex-repairing', 'failed', 'needs-native-riscv', 'needs-human', 'merged-pr', 'merged', 'discovered'];
let dashboard = null;
let inventory = null;
let inventoryPage = 0;
let searchTimer = null;
let historyPage = 0;

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined && text !== null) element.textContent = String(text);
  if (className) element.className = className;
  return element;
}

function safeLink(label, href, className) {
  if (!href) return node('span', label || '—');
  try {
    const url = new URL(href, window.location.href);
    if (!['https:', 'http:'].includes(url.protocol)) return node('span', label || '—');
    const link = node('a', label, className);
    link.href = url.href;
    link.rel = 'noopener noreferrer';
    return link;
  } catch (_) {
    return node('span', label || '—');
  }
}

function timeText(value) {
  if (!value) return 'never';
  const parsed = new Date(value);
  return Number.isNaN(parsed.valueOf()) ? 'unknown' : parsed.toLocaleString();
}

function compact(value) {
  return new Intl.NumberFormat(undefined, {notation: 'compact', maximumFractionDigits: 1}).format(value || 0);
}

function statusSort(a, b) {
  const left = stateOrder.indexOf(a);
  const right = stateOrder.indexOf(b);
  return (left < 0 ? 999 : left) - (right < 0 ? 999 : right) || a.localeCompare(b);
}

function gapSummary(reasons) {
  const groups = new Map();
  for (const item of reasons || []) {
    const label = String(typeof item === 'string' ? item : item.reason || 'unspecified gap').slice(0, 100);
    const count = typeof item === 'object' && Number.isInteger(item.count) && item.count > 0 ? item.count : 1;
    groups.set(label, (groups.get(label) || 0) + count);
  }
  return [...groups.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5).map(([label, count]) => `${label}: ${count}`).join('; ');
}

function renderSummary() {
  const container = document.querySelector('#summary');
  container.replaceChildren();
  const counts = inventory.status_counts || {};
  const history = dashboard.build_history || {};
  const metrics = history.metrics || {};
  const totals = [
    ['Inventory entries', inventory.entries.length],
    ['Managed', dashboard.packages.length],
    ['Cumulative build + smoke success', history.source_generated_at ? `${history.lower_bound ? '≥ ' : ''}${metrics.cumulative_success_packages}` : 'unknown'],
    ['Current main recipe ever succeeded', history.source_generated_at ? `${history.lower_bound ? '≥ ' : ''}${metrics.current_main_success_packages}` : 'unknown'],
    ['Current open PR success', history.source_generated_at && history.current_pr_source_available ? `${history.lower_bound ? '≥ ' : ''}${metrics.current_pr_success_packages}` : 'unknown'],
    ['Published packages', metrics.published_packages === null || metrics.published_packages === undefined ? (metrics.observed_published_packages ? `≥ ${metrics.observed_published_packages} (partial)` : 'unknown') : metrics.published_packages],
    ['Open / repairing inventory rows', (counts['open-pr'] || 0) + (counts['pr-open'] || 0) + (counts['repair-queued'] || 0) + (counts['codex-repairing'] || 0)],
    ['Needs native inventory rows', counts['needs-native-riscv'] || 0],
  ];
  for (const [label, value] of totals) {
    const card = node('article', null, 'card');
    card.append(node('strong', typeof value === 'number' ? compact(value) : value), node('span', label));
    card.title = String(value);
    container.append(card);
  }
  const reasons = gapSummary(history.reasons);
  const publicationFiles = history.publication_files || {};
  const publicationGaps = gapSummary(history.publication_gaps);
  document.querySelector('#history-coverage').textContent = `History collected ${timeText(history.source_generated_at)} · cutoff ${timeText(history.cutoff)} · ${history.coverage_complete ? 'available-history scan complete' : 'partial / unavailable history, counts are lower bounds'}. Current PR snapshot: ${history.current_pr_source_available ? timeText(history.current_pr_source_generated_at) : 'unavailable / incomplete; count unknown'}. Publication coverage: ${history.publication_coverage || 'unavailable'}, collected ${timeText(history.publication_source_generated_at)}, verified files ${publicationFiles.verified_files ?? 'unknown'} / ${publicationFiles.rpm_files == null || publicationFiles.srpm_files == null ? 'unknown' : publicationFiles.rpm_files + publicationFiles.srpm_files}. Counts do not restore deleted Actions history or remove the self-hosted fleet trust gate.`;
  document.querySelector('#coverage-gap-summary').textContent = `History gap records ${(history.reasons || []).length}, top categories: ${reasons || 'none'}. Publication gap records ${(history.publication_gaps || []).length}, top categories: ${publicationGaps || 'none'}. Full unabridged records, including run/head and payload checksums, remain in the downloadable evidence JSON.`;
}

function renderBuildHistory() {
  const history = dashboard.build_history || {};
  const query = document.querySelector('#history-search').value.trim().toLowerCase();
  const filter = document.querySelector('#history-evidence').value;
  const all = history.packages || [];
  const rows = all.filter(item => (!query || `${item.package_id}\n${item.name}`.toLowerCase().includes(query)) && (!filter || (filter === 'ever' && item.ever_succeeded) || (filter === 'main' && item.current_main_recipe_succeeded) || (filter === 'pr' && item.current_pr_status === 'passed') || (filter === 'published' && item.published)));
  const pageCount = Math.max(1, Math.ceil(rows.length / 100));
  historyPage = Math.min(historyPage, pageCount - 1);
  const body = document.querySelector('#history-rows');
  body.replaceChildren();
  for (const item of rows.slice(historyPage * 100, (historyPage + 1) * 100)) {
    const row = node('tr');
    const identity = node('td', item.package_id);
    identity.append(node('small', item.on_current_main ? 'on current main' : 'historical / PR-only; not on current main'));
    const main = node('td', `${item.current_main_recipe_succeeded ? 'recipe historically succeeded' : 'recipe success not observed'} · latest known CI: ${item.current_main_status}`);
    if (item.current_recipe_tree_sha) main.append(node('small', `tree ${item.current_recipe_tree_sha}`));
    const pr = node('td', item.current_pr_status);
    if (item.current_pr_head_sha) pr.append(node('small', `head ${item.current_pr_head_sha}`));
    const evidence = node('td', timeText(item.last_success_at));
    evidence.append(safeLink('Last successful run', item.last_success_run_url));
    if ((item.observations || []).length) {
      const details = node('details');
      details.append(node('summary', `${item.success_observation_count} successful observations (not package count)`));
      details.addEventListener('toggle', () => {
        if (!details.open || details.dataset.loaded) return;
        for (const observation of item.observations) {
          const fact = node('p');
          fact.append(safeLink(`Run ${observation.run_id}, attempt ${observation.run_attempt}`, observation.run_url), node('small', `${timeText(observation.completed_at)} · ${observation.event} / ${observation.head_branch || 'unknown branch'} · ${observation.evidence_strength} · recipe ${observation.recipe_tree_sha} · head ${observation.head_sha}`));
          for (const kind of ['build', 'smoke']) {
            const job = observation.jobs && observation.jobs[kind];
            if (job && Number.isInteger(job.id) && job.id > 0 && observation.run_url) fact.append(safeLink(`${kind} job`, `${observation.run_url}/job/${job.id}`), document.createTextNode(' · '));
          }
          details.append(fact);
        }
        details.dataset.loaded = 'true';
      });
      evidence.append(details);
    }
    const publication = node('td', item.published ? 'verified live availability (any version)' : 'unavailable / unverified');
    if (item.published) {
      publication.append(node('small', (item.publication.versions || []).map(version => `${version.epoch}:${version.version}-${version.release}`).join(', ')));
      publication.append(safeLink('Generation state', item.publication.state));
      for (const url of item.publication.srpm || []) publication.append(safeLink('SRPM', url));
      for (const url of item.publication.rpm || []) publication.append(safeLink('RPM', url));
    }
    [identity, node('td', item.ever_succeeded ? 'succeeded at least once' : 'not observed'), main, pr, publication, evidence].forEach(cell => row.append(cell));
    body.append(row);
  }
  document.querySelector('#history-empty').hidden = rows.length !== 0;
  document.querySelector('#history-result-count').textContent = `${rows.length} matching canonical packages · page ${historyPage + 1}/${pageCount}`;
  document.querySelector('#history-prev').disabled = historyPage === 0;
  document.querySelector('#history-next').disabled = historyPage >= pageCount - 1;
}

function renderHealth() {
  const health = dashboard.update_health || {};
  const container = document.querySelector('#update-health');
  container.replaceChildren();
  const coverage = Number(health.coverage_percent || 0);
  const items = [
    ['Schedule', timeText(health.last_scheduled_at)],
    ['Coverage', health.source_available ? `${health.checked || 0}/${health.expected || 0} (${coverage.toFixed(1)}%)` : 'unknown'],
    ['Failed shards', health.source_available ? health.failed_shards || 0 : 'unknown'],
    ['Pending backfill', health.source_available ? health.due_rechecks || 0 : 'unknown'],
    ['Completed', timeText(health.last_completed_at)],
  ];
  for (const [label, value] of items) {
    const item = node('div', null, 'health-item');
    item.append(node('span', label), node('strong', value));
    container.append(item);
  }
  container.dataset.complete = health.source_available ? String((health.failed_shards || 0) === 0 && (health.due_rechecks || 0) === 0) : 'unknown';
}

function fillSelect(selector, values) {
  const select = document.querySelector(selector);
  for (const value of values) {
    const option = node('option', value);
    option.value = value;
    select.append(option);
  }
}

function fillFilters() {
  fillSelect('#inventory-status', [...new Set(inventory.entries.map(item => item.status))].sort(statusSort));
  fillSelect('#managed-status', [...new Set(dashboard.packages.map(item => item.status))].sort(statusSort));
}

function inventoryMatches(item) {
  const query = document.querySelector('#inventory-search').value.trim().toLowerCase();
  const status = document.querySelector('#inventory-status').value;
  const evidence = document.querySelector('#inventory-evidence').value;
  if (status && item.status !== status) return false;
  if (query) {
    const haystack = [item.inventory_id, item.package_id, item.name, ...(item.aliases || []), ...(item.component_ids || []), ...(item.decisions || [])].filter(Boolean).join('\n').toLowerCase();
    if (!haystack.includes(query)) return false;
  }
  const links = item.links || {};
  const published = (links.rpm || []).length > 0 && (links.srpm || []).length > 0;
  if (evidence === 'published' && !published) return false;
  if (evidence === 'ci' && (!links.ci || published)) return false;
  if (evidence === 'none' && (published || links.ci)) return false;
  return true;
}

function appendArtifactLinks(cell, item) {
  const links = item.links || {};
  const pieces = [];
  if (links.pr) pieces.push(['PR', links.pr, 'evidence-link']);
  if (links.ci) pieces.push(['CI', links.ci, 'evidence-link']);
  for (const [index, href] of (links.rpm || []).entries()) pieces.push([`RPM${(links.rpm || []).length > 1 ? ` ${index + 1}` : ''}`, href, 'artifact-link']);
  for (const [index, href] of (links.srpm || []).entries()) pieces.push([`SRPM${(links.srpm || []).length > 1 ? ` ${index + 1}` : ''}`, href, 'artifact-link']);
  if (!pieces.length) {
    cell.append(node('span', 'inventory metadata only', 'muted'));
    return;
  }
  pieces.forEach(([label, href, className], index) => {
    if (index) cell.append(document.createTextNode(' · '));
    cell.append(safeLink(label, href, className));
  });
}

function renderInventoryRows() {
  const body = document.querySelector('#inventory-rows');
  body.replaceChildren();
  const filtered = inventory.entries.filter(inventoryMatches);
  const size = Number(document.querySelector('#inventory-page-size').value || 100);
  const pageCount = Math.max(1, Math.ceil(filtered.length / size));
  inventoryPage = Math.min(inventoryPage, pageCount - 1);
  const start = inventoryPage * size;
  for (const item of filtered.slice(start, start + size)) {
    const row = document.createElement('tr');
    const packageCell = document.createElement('td');
    packageCell.append(safeLink(item.name, item.links && (item.links.package || item.links.upstream)));
    if (item.package_id && item.package_id !== item.name) packageCell.append(node('small', item.package_id));
    const stateCell = document.createElement('td');
    stateCell.append(node('span', item.status, `badge state-${item.status}`));
    const componentCell = document.createElement('td');
    componentCell.append(node('span', (item.component_ids || []).slice(0, 3).join(', ') || '—'));
    if ((item.decisions || []).length) componentCell.append(node('small', item.decisions.join(', ')));
    const evidenceCell = document.createElement('td');
    appendArtifactLinks(evidenceCell, item);
    [packageCell, stateCell, node('td', item.version), componentCell, node('td', timeText(item.updated_at)), evidenceCell].forEach(cell => row.append(cell));
    if (item.summary) row.title = item.summary;
    body.append(row);
  }
  const end = Math.min(start + size, filtered.length);
  document.querySelector('#inventory-result-count').textContent = filtered.length ? `${start + 1}–${end} of ${filtered.length} (page ${inventoryPage + 1}/${pageCount})` : `0 of ${inventory.entries.length}`;
  document.querySelector('#inventory-empty').hidden = filtered.length !== 0;
  document.querySelector('#inventory-prev').disabled = inventoryPage === 0;
  document.querySelector('#inventory-next').disabled = inventoryPage >= pageCount - 1;
}

function managedMatches(item) {
  const query = document.querySelector('#managed-search').value.trim().toLowerCase();
  const status = document.querySelector('#managed-status').value;
  const lag = document.querySelector('#managed-lag').value;
  const patch = document.querySelector('#managed-patch').value;
  if (query && ![item.package_id, item.name, ...(item.sources || [])].join('\n').toLowerCase().includes(query)) return false;
  if (status && item.status !== status) return false;
  if (lag === 'lag' && (!item.latest_upstream_version || item.current_version === item.latest_upstream_version)) return false;
  if (lag === 'current' && (!item.latest_upstream_version || item.current_version !== item.latest_upstream_version)) return false;
  if (patch === 'yes' && !item.patch_count) return false;
  if (patch === 'no' && item.patch_count) return false;
  return true;
}

function renderManagedRows() {
  const body = document.querySelector('#managed-rows');
  body.replaceChildren();
  const filtered = dashboard.packages.filter(managedMatches);
  for (const item of filtered) {
    const row = document.createElement('tr');
    const packageCell = document.createElement('td');
    packageCell.append(safeLink(item.name, item.links && item.links.package));
    const stateCell = document.createElement('td');
    stateCell.append(node('span', item.status, `badge state-${item.status}`));
    const evidenceCell = document.createElement('td');
    appendArtifactLinks(evidenceCell, item);
    [packageCell, stateCell, node('td', item.current_version), node('td', item.latest_upstream_version), node('td', (item.sources || []).join(', ') || 'unknown'), node('td', item.riscv_status), node('td', item.patch_count), evidenceCell].forEach(cell => row.append(cell));
    if (item.last_error) row.title = item.last_error;
    body.append(row);
  }
  document.querySelector('#managed-result-count').textContent = `${filtered.length} of ${dashboard.packages.length}`;
  document.querySelector('#managed-empty').hidden = filtered.length !== 0;
}

function resetInventoryPage() {
  inventoryPage = 0;
  window.clearTimeout(searchTimer);
  searchTimer = window.setTimeout(renderInventoryRows, 120);
}

async function start() {
  const dashboardResponse = await fetch('data.json', {cache: 'no-store'});
  if (!dashboardResponse.ok) throw new Error(`dashboard data request failed: ${dashboardResponse.status}`);
  dashboard = await dashboardResponse.json();
  const inventoryResponse = await fetch((dashboard.inventory && dashboard.inventory.url) || 'inventory.json', {cache: 'no-store'});
  if (!inventoryResponse.ok) throw new Error(`inventory request failed: ${inventoryResponse.status}`);
  inventory = await inventoryResponse.json();
  document.querySelector('#coverage-note').textContent = dashboard.coverage_claim === 'full-package-inventory'
    ? `${inventory.entries.length.toLocaleString()} inventory entries from the committed snapshot plus managed/PR identity overlays; build steps and public payloads have separate evidence gates.`
    : 'Only observed managed packages are available; full inventory input was missing.';
  document.querySelector('#generated-at').textContent = `Dashboard generated ${timeText(dashboard.generated_at)}`;
  document.querySelector('#snapshot-note').textContent = `Inventory snapshot ${inventory.source.snapshot_id || 'unknown'} · source generated ${timeText(inventory.source.generated_at)}`;
  renderSummary();
  renderBuildHistory();
  renderHealth();
  fillFilters();
  renderInventoryRows();
  renderManagedRows();
  document.querySelector('#inventory-filters').addEventListener('input', resetInventoryPage);
  document.querySelector('#inventory-filters').addEventListener('reset', () => window.setTimeout(() => { inventoryPage = 0; renderInventoryRows(); }, 0));
  document.querySelector('#inventory-prev').addEventListener('click', () => { inventoryPage -= 1; renderInventoryRows(); });
  document.querySelector('#inventory-next').addEventListener('click', () => { inventoryPage += 1; renderInventoryRows(); });
  document.querySelector('#managed-filters').addEventListener('input', renderManagedRows);
  document.querySelector('#managed-filters').addEventListener('reset', () => window.setTimeout(renderManagedRows, 0));
  document.querySelector('#history-filters').addEventListener('input', () => { historyPage = 0; renderBuildHistory(); });
  document.querySelector('#history-filters').addEventListener('reset', () => window.setTimeout(() => { historyPage = 0; renderBuildHistory(); }, 0));
  document.querySelector('#history-prev').addEventListener('click', () => { historyPage -= 1; renderBuildHistory(); });
  document.querySelector('#history-next').addEventListener('click', () => { historyPage += 1; renderBuildHistory(); });
}

start().catch(error => {
  document.querySelector('#coverage-note').textContent = `Dashboard generation or loading failed: ${error.message}`;
});
