"""Face analysis request and response boundaries."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from client import FaceAnalyzeClient, FaceError


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.headers = {"x-request-id": "trace-face"}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, *_):
        return json.dumps(self.payload).encode()


@pytest.mark.asyncio
async def test_analyze_posts_once_and_omits_internal_fields():
    calls = []

    def fake_open(request, timeout):
        calls.append((request.full_url, json.loads(request.data), timeout))
        return FakeResponse(
            {
                "image_width": 1024,
                "image_height": 1024,
                "face_model_version": "3.0",
                "face_shape_set": [{"landmarks": [1, 2]}],
                "supplier": "internal-only",
            }
        )

    with patch("client.OPENER.open", side_effect=fake_open):
        result = await FaceAnalyzeClient("test-key").analyze(
            "https://example.org/portrait.jpg", 1
        )
    assert calls == [
        (
            "https://api.acedata.cloud/face/analyze",
            {"image_url": "https://example.org/portrait.jpg", "mode": 1},
            60,
        )
    ]
    assert result["status"] == "succeeded"
    assert result["trace_id"] == "trace-face"
    assert result["face_count"] == 1
    assert result["face_shape_set"] == [{"landmarks": [1, 2]}]
    assert "supplier" not in result


@pytest.mark.asyncio
async def test_non_https_image_is_rejected_before_request():
    with patch("client.OPENER.open") as opening, pytest.raises(FaceError):
        await FaceAnalyzeClient("test-key").analyze("http://example.org/a.jpg")
    assert opening.call_count == 0
