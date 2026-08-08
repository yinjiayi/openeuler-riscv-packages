// SPDX-License-Identifier: Apache-2.0
'use strict';

const stateOrder = ['discovered', 'pr-open', 'ci-queued', 'building', 'repair-queued', 'codex-repairing', 'failed', 'needs-native-riscv', 'needs-human', 'passed', 'merged'];
let dashboard = null;

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined && text !== null) element.textContent = String(text);
  if (className) element.className = className;
  return element;
}

function safeLink(label, href) {
  if (!href) return node('span', '—');
  try {
    const url = new URL(href, window.location.href);
    if (!['https:', 'http:'].includes(url.protocol)) return node('span', '—');
    const link = node('a', label);
    link.href = url.href;
    link.rel = 'noopener noreferrer';
    return link;
  } catch (_) {
    return node('span', '—');
  }
}

function timeText(value) {
  if (!value) return 'never';
  const parsed = new Date(value);
  return Number.isNaN(parsed.valueOf()) ? 'unknown' : parsed.toLocaleString();
}

function renderSummary() {
  const container = document.querySelector('#summary');
  container.replaceChildren();
  const totals = [['Managed', dashboard.packages.length], ['Behind upstream', dashboard.packages.filter(item => item.latest_upstream_version && item.current_version !== item.latest_upstream_version).length], ['With patches', dashboard.packages.filter(item => item.patch_count).length]];
  for (const [label, value] of totals) {
    const card = node('article', null, 'card');
    card.append(node('strong', value), node('span', label));
    container.append(card);
  }
  for (const state of stateOrder) {
    const value = dashboard.packages.filter(item => item.status === state).length;
    if (!value) continue;
    const card = node('article', null, `card state-${state}`);
    card.append(node('strong', value), node('span', state));
    container.append(card);
  }
}

function renderHealth() {
  const health = dashboard.update_health || {};
  const container = document.querySelector('#update-health');
  container.replaceChildren();
  const coverage = Number(health.coverage_percent || 0);
  const items = [
    ['Schedule', timeText(health.last_scheduled_at)],
    ['Coverage', `${health.checked || 0}/${health.expected || 0} (${coverage.toFixed(1)}%)`],
    ['Failed shards', health.failed_shards || 0],
    ['Pending backfill', health.due_rechecks || 0],
    ['Completed', timeText(health.last_completed_at)],
    ['Consecutive missed days', health.consecutive_missed_days || 0],
  ];
  for (const [label, value] of items) {
    const item = node('div', null, 'health-item');
    item.append(node('span', label), node('strong', value));
    container.append(item);
  }
  container.dataset.complete = String((health.failed_shards || 0) === 0 && (health.due_rechecks || 0) === 0);
}

function fillFilters() {
  const statuses = [...new Set(dashboard.packages.map(item => item.status))].sort((a, b) => stateOrder.indexOf(a) - stateOrder.indexOf(b));
  const failures = [...new Set(dashboard.packages.map(item => item.failure_category).filter(Boolean))].sort();
  const status = document.querySelector('#status-filter');
  const failure = document.querySelector('#failure-filter');
  for (const value of statuses) {
    const option = node('option', value);
    option.value = value;
    status.append(option);
  }
  for (const value of failures) {
    const option = node('option', value);
    option.value = value;
    failure.append(option);
  }
}

function matches(item) {
  const status = document.querySelector('#status-filter').value;
  const source = document.querySelector('#source-filter').value.trim().toLowerCase();
  const lag = document.querySelector('#lag-filter').value;
  const patch = document.querySelector('#patch-filter').value;
  const failure = document.querySelector('#failure-filter').value;
  const days = Number(document.querySelector('#age-filter').value || 0);
  if (status && item.status !== status) return false;
  if (source && !(item.sources || []).some(value => value.toLowerCase().includes(source))) return false;
  if (lag === 'lag' && (!item.latest_upstream_version || item.current_version === item.latest_upstream_version)) return false;
  if (lag === 'current' && (!item.latest_upstream_version || item.current_version !== item.latest_upstream_version)) return false;
  if (patch === 'yes' && !item.patch_count) return false;
  if (patch === 'no' && item.patch_count) return false;
  if (failure && item.failure_category !== failure) return false;
  if (days) {
    const updated = new Date(item.updated_at || 0).valueOf();
    if (!updated || Date.now() - updated > days * 86400000) return false;
  }
  return true;
}

function renderRows() {
  const body = document.querySelector('#package-rows');
  body.replaceChildren();
  const filtered = dashboard.packages.filter(matches);
  for (const item of filtered) {
    const row = document.createElement('tr');
    const packageCell = document.createElement('td');
    packageCell.append(safeLink(item.name, item.links && item.links.package));
    const stateCell = document.createElement('td');
    stateCell.append(node('span', item.status, `badge state-${item.status}`));
    if (item.failure_category) stateCell.append(node('small', item.failure_category));
    const evidence = document.createElement('td');
    if (item.links && item.links.pr) evidence.append(safeLink('PR', item.links.pr));
    else evidence.append(node('span', 'metadata only'));
    if (item.links && item.links.logs) evidence.append(document.createTextNode(' · '), safeLink('log', item.links.logs));
    const values = [
      packageCell,
      stateCell,
      node('td', item.current_version),
      node('td', item.latest_upstream_version),
      node('td', (item.sources || []).join(', ') || 'unknown'),
      node('td', item.riscv_status),
      node('td', item.patch_count),
      node('td', timeText(item.updated_at)),
      evidence,
    ];
    values.forEach(cell => row.append(cell));
    if (item.last_error) row.title = item.last_error;
    body.append(row);
  }
  document.querySelector('#result-count').textContent = `${filtered.length} of ${dashboard.packages.length}`;
  document.querySelector('#empty').hidden = filtered.length !== 0;
}

async function start() {
  const response = await fetch('data.json', {cache: 'no-store'});
  if (!response.ok) throw new Error(`dashboard data request failed: ${response.status}`);
  dashboard = await response.json();
  document.querySelector('#coverage-note').textContent = dashboard.coverage_claim === 'observed-managed-packages-only' ? 'Observed managed packages only; this dashboard does not claim complete ecosystem coverage.' : dashboard.coverage_claim;
  document.querySelector('#generated-at').textContent = `Generated ${timeText(dashboard.generated_at)}`;
  document.querySelector('#snapshot-note').textContent = 'Candidates are deduplicated by official upstream stable release component.';
  renderSummary();
  renderHealth();
  fillFilters();
  renderRows();
  const form = document.querySelector('#filters');
  form.addEventListener('input', renderRows);
  form.addEventListener('reset', () => window.setTimeout(renderRows, 0));
}

start().catch(error => {
  document.querySelector('#coverage-note').textContent = `Dashboard generation or loading failed: ${error.message}`;
});
