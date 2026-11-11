# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import io
import http.client
import json
import os
import pathlib
import runpy
import tempfile
import traceback
import unittest
import urllib.error
from unittest import mock

from helpers import SCRIPTS


URL = "https://api.github.com/repos/example/project/tags"
TOKEN = "test-only-process-credential"


class Response:
    def __init__(self, data=b"[]", url=URL, status=200, headers=None):
        self.data = io.BytesIO(data)
        self.url = url
        self.status = self.code = status
        self.headers = headers or {}
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def read(self, count):
        return self.data.read(count)

    def geturl(self):
        return self.url

    def close(self):
        self.closed = True


class UpdateGitHubAuthTests(unittest.TestCase):
    def setUp(self):
        self.module = runpy.run_path(str(SCRIPTS / "_lib.py"))
        self.fetch = self.module["fetch_url"]
        self.error = self.module["ToolError"]
        self.environment = mock.patch.dict(os.environ, {"GH_TOKEN": TOKEN})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def transport(self, authenticated=None, plain=None):
        opener = mock.Mock()
        opener.open.side_effect = authenticated or (lambda request, **kw: Response(url=request.full_url))
        build = mock.Mock(return_value=opener)
        urlopen = mock.Mock(side_effect=plain or (lambda request, **kw: Response(url=request.full_url)))
        patch = mock.patch.multiple(self.module["urllib"].request, build_opener=build, urlopen=urlopen)
        patch.start()
        self.addCleanup(patch.stop)
        return opener.open, urlopen, build

    def test_opt_in_metadata_auth_present_and_not_in_cache_or_metadata(self):
        authenticated, plain, build = self.transport()
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            data, metadata = self.fetch(URL, github_api_metadata=True, cache_dir=root)
            request = authenticated.call_args.args[0]
            self.assertEqual(request.get_header("Authorization"), "Bearer " + TOKEN)
            self.assertEqual(request.get_header("Accept"), "application/vnd.github+json")
            self.assertEqual(data, b"[]")
            self.assertNotIn(TOKEN, json.dumps(metadata))
            self.assertTrue(list(root.iterdir()))
            for path in root.iterdir():
                self.assertNotIn(TOKEN.encode(), path.read_bytes())
        plain.assert_not_called()
        self.assertIsInstance(build.call_args.args[0], self.module["_RejectGitHubMetadataRedirects"])

    def test_token_absent_uses_existing_unauthenticated_transport(self):
        authenticated, plain, build = self.transport()
        with mock.patch.dict(os.environ, {"GH_TOKEN": ""}):
            self.fetch(URL, github_api_metadata=True)
        self.assertIsNone(plain.call_args.args[0].get_header("Authorization"))
        authenticated.assert_not_called()
        build.assert_not_called()

    def test_default_and_source_archive_requests_never_receive_token(self):
        authenticated, plain, build = self.transport()
        for url in (URL, "https://github.com/example/project/archive/refs/tags/v2.tar.gz",
                    "https://codeload.github.com/example/project/tar.gz/v2",
                    "https://api.github.com/repos/example/project/tarball/v2",
                    "https://example.org/source.tar.gz"):
            self.fetch(url)
            self.assertIsNone(plain.call_args.args[0].get_header("Authorization"))
        authenticated.assert_not_called()
        build.assert_not_called()

    def test_invalid_origin_or_nonmetadata_opt_in_rejected_before_request(self):
        authenticated, plain, build = self.transport()
        for url in ("https://example.org/repos/o/r/tags", "https://api.github.com.evil.test/repos/o/r/tags",
                    "https://api.github.com@evil.test/repos/o/r/tags", "https://user@api.github.com/repos/o/r/tags",
                    "https://api.github.com:8443/repos/o/r/tags", "http://api.github.com/repos/o/r/tags",
                    URL + "#fragment", "https://api.github.com/repos/o/r/releases/assets/1",
                    "https://api.github.com/repos/o/r/tarball/v1", "https://api.github.com/repos/o/r/zipball/v1"):
            with self.subTest(url=url), self.assertRaises(self.error):
                self.fetch(url, github_api_metadata=True)
        authenticated.assert_not_called()
        plain.assert_not_called()
        build.assert_not_called()

    def test_metadata_route_allowlist_is_exact(self):
        accept = self.module["github_metadata_url"]
        for path in ("tags", "releases", "releases/latest", "git/refs/tags"):
            self.assertTrue(accept("https://api.github.com/repos/o/r/" + path + "?per_page=100"))
        self.assertTrue(accept("https://api.github.com:443/repos/o/r/tags"))
        self.assertFalse(accept("https://api.github.com/repos/o/r/tags/../tarball/v1"))

    def test_all_authenticated_3xx_are_rejected_without_redirect_following(self):
        handler = self.module["_RejectGitHubMetadataRedirects"]()
        request = self.module["urllib"].request.Request(URL, headers={"Authorization": "Bearer " + TOKEN})
        for status in range(300, 400):
            response = Response(status=status, headers={"Location": "https://evil.test/"})
            with self.subTest(status=status), self.assertRaisesRegex(self.error, "3xx") as raised:
                handler.https_response(request, response)
            self.assertTrue(response.closed)
            self.assertNotIn(TOKEN, str(raised.exception))

    def test_authenticated_response_url_change_is_fatal(self):
        authenticated, plain, _ = self.transport(authenticated=lambda request, **kw: Response(url="https://evil.test/"))
        with self.assertRaises(self.error) as raised:
            self.fetch(URL, github_api_metadata=True)
        self.assertEqual(authenticated.call_count, 1)
        plain.assert_not_called()
        self.assertNotIn(TOKEN, str(raised.exception))

    def test_403_is_not_retried_and_error_does_not_echo_response_or_token(self):
        def forbidden(request, **kw):
            raise urllib.error.HTTPError(URL, 403, TOKEN, {"Retry-After": "1"}, io.BytesIO(TOKEN.encode()))
        authenticated, plain, _ = self.transport(authenticated=forbidden)
        try:
            self.fetch(URL, github_api_metadata=True, retries=3)
        except self.error as exc:
            self.assertIn("HTTP 403", str(exc))
            self.assertNotIn(TOKEN, traceback.format_exc())
        else:
            self.fail("expected authenticated HTTP failure")
        self.assertEqual(authenticated.call_count, 1)
        plain.assert_not_called()

    def test_retryable_http_error_traceback_is_credential_safe(self):
        def unavailable(request, **kw):
            raise urllib.error.HTTPError(URL, 503, TOKEN, {}, io.BytesIO(TOKEN.encode()))
        authenticated, _, _ = self.transport(authenticated=unavailable)
        with mock.patch("time.sleep"):
            try:
                self.fetch(URL, github_api_metadata=True, retries=1)
            except self.error as exc:
                self.assertIn("HTTP 503", str(exc))
                self.assertNotIn(TOKEN, traceback.format_exc())
            else:
                self.fail("expected authenticated HTTP failure")
        self.assertEqual(authenticated.call_count, 2)

    def test_reflected_token_body_or_header_is_rejected_without_cache(self):
        cases = ((TOKEN.encode(), {}), (b"[]", {"ETag": TOKEN}),
                 (b"[]", {"Last-Modified": TOKEN}), (b"[]", {"X-Other": TOKEN}))
        for data, headers in cases:
            with self.subTest(headers=headers), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                response = Response(data, headers=headers)
                authenticated, _, _ = self.transport(authenticated=lambda request, **kw: response)
                try:
                    self.fetch(URL, github_api_metadata=True, cache_dir=root)
                except self.error:
                    self.assertNotIn(TOKEN, traceback.format_exc())
                else:
                    self.fail("expected reflected credential rejection")
                self.assertEqual(authenticated.call_count, 1)
                self.assertEqual(list(root.iterdir()), [])
                self.assertTrue(response.closed)

    def test_invalid_credential_controls_rejected_before_transport(self):
        authenticated, plain, build = self.transport()
        for credential in (TOKEN + "\n", "\r" + TOKEN, TOKEN + "\x00", TOKEN + "\t", TOKEN + "é"):
            # A real OS environment rejects NUL before fetch_url can see it.
            # Use an inert mapping so the validator itself is exercised too.
            with mock.patch.object(self.module["os"], "environ", {"GH_TOKEN": credential}):
                with self.assertRaisesRegex(self.error, "invalid process"):
                    self.fetch(URL, github_api_metadata=True)
        authenticated.assert_not_called()
        plain.assert_not_called()
        build.assert_not_called()

    def test_authenticated_network_error_is_credential_safe(self):
        authenticated, _, _ = self.transport(authenticated=mock.Mock(side_effect=urllib.error.URLError(TOKEN)))
        with self.assertRaises(self.error) as raised:
            self.fetch(URL, github_api_metadata=True, retries=0)
        self.assertEqual(authenticated.call_count, 1)
        self.assertNotIn(TOKEN, str(raised.exception))

    def test_authenticated_bad_status_traceback_and_cache_are_credential_safe(self):
        authenticated, _, _ = self.transport(authenticated=mock.Mock(side_effect=http.client.BadStatusLine(TOKEN)))
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            try:
                self.fetch(URL, github_api_metadata=True, retries=3, cache_dir=root)
            except self.error as exc:
                self.assertIn("BadStatusLine", str(exc))
                self.assertNotIn(TOKEN, traceback.format_exc())
            else:
                self.fail("expected authenticated protocol rejection")
            self.assertEqual(list(root.iterdir()), [])
        self.assertEqual(authenticated.call_count, 1)

    def test_bad_status_scan_failure_json_does_not_persist_credential(self):
        self.transport(authenticated=mock.Mock(side_effect=http.client.BadStatusLine(TOKEN)))
        module = runpy.run_path(str(SCRIPTS / "check-update"))
        scan = module["scan_package"]
        def feed(*args, **kwargs):
            return self.fetch(URL, github_api_metadata=True, retries=0, cache_dir=kwargs["cache_dir"])
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            with mock.patch.dict(scan.__globals__, {"load_release_feed": feed, "ToolError": self.error}):
                result = scan({"package_id": "example", "current_version": "1", "release_api": URL},
                              now=self.module["utc_now"](), cache_dir=root, limiter=None,
                              timeout=1, retries=0, max_source_bytes=100, digest_sources=False)
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["failure"]["category"], "upstream-request")
            self.assertIn("BadStatusLine", result["failure"]["message"])
            self.assertNotIn(TOKEN, json.dumps(result))
            self.assertEqual(list(root.iterdir()), [])

    def test_unauthenticated_http_exception_behavior_is_unchanged(self):
        original = http.client.BadStatusLine("original protocol error")
        _, plain, _ = self.transport(plain=mock.Mock(side_effect=original))
        with self.assertRaises(http.client.BadStatusLine) as raised:
            self.fetch("https://example.org/releases.json")
        self.assertIs(raised.exception, original)
        self.assertEqual(plain.call_count, 1)

    def test_non_github_conditional_cache_and_304_behavior_unchanged(self):
        url = "https://example.org/releases.json"
        def initial(request, **kw):
            self.assertIsNone(request.get_header("Authorization"))
            return Response(b"[]", url, headers={"ETag": '"v1"', "Last-Modified": "Wed, 21 Oct 2026 00:00:00 GMT"})
        _, plain, build = self.transport(plain=initial)
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            self.fetch(url, cache_dir=root)
            def unchanged(request, **kw):
                self.assertEqual(request.get_header("If-none-match"), '"v1"')
                self.assertEqual(request.get_header("If-modified-since"), "Wed, 21 Oct 2026 00:00:00 GMT")
                self.assertIsNone(request.get_header("Authorization"))
                raise urllib.error.HTTPError(url, 304, "Not Modified", {}, None)
            plain.side_effect = unchanged
            data, metadata = self.fetch(url, cache_dir=root)
            self.assertEqual(data, b"[]")
            self.assertTrue(metadata["cached"])
            self.assertEqual(metadata["status"], 304)
            self.assertNotIn(TOKEN, json.dumps(metadata))
        build.assert_not_called()

    def test_authenticated_metadata_does_not_reuse_conditional_cache(self):
        def response(request, **kw):
            self.assertIsNone(request.get_header("If-none-match"))
            self.assertIsNone(request.get_header("If-modified-since"))
            return Response(headers={"ETag": '"v1"'})
        authenticated, _, _ = self.transport(authenticated=response)
        with tempfile.TemporaryDirectory() as directory:
            self.fetch(URL, github_api_metadata=True, cache_dir=pathlib.Path(directory))
            self.fetch(URL, github_api_metadata=True, cache_dir=pathlib.Path(directory))
        self.assertEqual(authenticated.call_count, 2)

    def test_load_location_propagates_explicit_metadata_opt_in(self):
        fetch = mock.Mock(return_value=(b"[]", {"status": 200}))
        function = self.module["load_location"]
        with mock.patch.dict(function.__globals__, {"fetch_url": fetch}):
            function(URL, github_api_metadata=True)
        self.assertIs(fetch.call_args.kwargs["github_api_metadata"], True)

    def test_both_feed_paths_opt_in_but_source_digest_does_not(self):
        module = runpy.run_path(str(SCRIPTS / "check-update"))
        feed = module["load_release_feed"]
        kwargs = dict(timeout=1, retries=0, cache_dir=None, limiter=None)
        fetch = mock.Mock(return_value=(b'[{"name":"v2.0"}]', {}))
        location = mock.Mock(return_value=([{"version": "2.0"}], {}))
        with mock.patch.dict(feed.__globals__, {"fetch_url": fetch, "load_location": location}):
            feed(URL, r"^v?(\d+[.]\d+)$", None, **kwargs)
            self.assertIs(fetch.call_args.kwargs["github_api_metadata"], True)
            feed(URL, None, None, **kwargs)
            self.assertIs(location.call_args.kwargs["github_api_metadata"], True)
            feed("https://api.github.com.evil.test/repos/o/r/tags", None, None, **kwargs)
            self.assertIs(location.call_args.kwargs["github_api_metadata"], False)
        digest = module["source_digest"]
        with mock.patch.dict(digest.__globals__, {"fetch_url": mock.Mock(return_value=(b"source", {}))}) as patched:
            digest("https://api.github.com/repos/o/r/tarball/v2", None, None, 1, 0, 100)
            self.assertNotIn("github_api_metadata", patched["fetch_url"].call_args.kwargs)

    def test_workflow_token_is_scoped_to_scan_step_read_permission(self):
        workflow = (SCRIPTS.parent / ".github/workflows/daily-update-check.yml").read_text()
        scan = workflow.split("  scan:\n", 1)[1].split("  aggregate:\n", 1)[0]
        self.assertIn("    permissions:\n      contents: read\n", scan)
        step = scan.split("      - name: Scan official stable releases", 1)[1].split("      - name:", 1)[0]
        self.assertIn("          GH_TOKEN: ${{ github.token }}\n", step)
        self.assertEqual(scan.count("GH_TOKEN:"), 1)
        self.assertNotIn("contents: write", scan)
