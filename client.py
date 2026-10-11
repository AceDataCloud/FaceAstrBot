"""Face keypoint analysis through the Ace Data Cloud API."""

from __future__ import annotations

import asyncio
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class FaceError(RuntimeError):
    """A user-facing error without credentials or upstream internals."""


class _NoRedirect(HTTPRedirectHandler):
    """Do not forward a key to any redirected destination."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        """Reject redirect responses.

        Args:
            request: Original request.
            fp: Response stream.
            code: Redirect HTTP status.
            msg: HTTP status text.
            headers: Redirect headers.
            newurl: Redirect target.

        Returns:
            None so urllib raises an HTTP error.
        """
        return


OPENER = build_opener(_NoRedirect)


class FaceAnalyzeClient:
    """Run one synchronous, read-only image analysis operation."""

    def __init__(self, api_key: str) -> None:
        """Keep the Ace Data Cloud API key only in memory.

        Args:
            api_key: Generation key with Face Analyze access.

        Raises:
            FaceError: If the key is missing or a management token.
        """
        token = api_key.strip()
        if (
            not token
            or token.lower().startswith("bearer ")
            or token.startswith("platform-")
        ):
            raise FaceError("Set an Ace Data Cloud key with Face Analyze access.")
        self._api_key = token

    def _analyze(self, image_url: str, mode: int) -> dict[str, Any]:
        """Send one Face Analyze request and keep only public result fields.

        Args:
            image_url: HTTPS image owned or authorized by the caller.
            mode: Zero for every face; one for the largest face.

        Returns:
            Image dimensions, face count, and at most three face-shape entries.

        Raises:
            FaceError: If the service request or response is invalid.
        """
        request = Request(
            "https://api.acedata.cloud/face/analyze",
            data=json.dumps({"image_url": image_url, "mode": mode}).encode(),
            headers={
                "Authorization": "Bearer " + self._api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "AceDataCloudAstrBot/0.1.0",
            },
            method="POST",
        )
        try:
            with OPENER.open(request, timeout=60) as response:
                body = json.load(response)
                trace_id = response.headers.get(
                    "x-trace-id", ""
                ) or response.headers.get("x-request-id", "")
        except HTTPError as exc:
            raise FaceError(
                f"Ace Data Cloud returned HTTP {exc.code}. Check key access."
            ) from None
        except (URLError, TimeoutError, OSError):
            raise FaceError(
                "The API connection failed. Check request history before retrying."
            ) from None
        except (ValueError, UnicodeError):
            raise FaceError("The API returned invalid JSON.") from None
        if (
            not isinstance(body, dict)
            or body.get("success") is False
            or body.get("error")
        ):
            raise FaceError("Face analysis failed. Check request history for details.")
        faces = body.get("face_shape_set", [])
        if not isinstance(faces, list):
            raise FaceError("The API returned an unexpected face result format.")
        return {
            "status": "succeeded",
            "success": True,
            "trace_id": str(body.get("trace_id") or trace_id),
            "image_width": body.get("image_width"),
            "image_height": body.get("image_height"),
            "face_model_version": body.get("face_model_version"),
            "face_count": len(faces),
            "face_shape_set": faces[:3],
        }

    async def analyze(self, image_url: str, mode: int = 1) -> dict[str, Any]:
        """Analyze an authorized HTTPS image without blocking AstrBot.

        Args:
            image_url: Public HTTPS image URL; the plugin does not upload files.
            mode: Zero analyzes all faces; one analyzes the largest face.

        Returns:
            Structured analysis, including face keypoints.

        Raises:
            FaceError: For unsupported input or service failures.
        """
        parsed = urlsplit(image_url)
        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or parsed.username
            or parsed.password
        ):
            raise FaceError(
                "Provide an HTTPS image URL that you are authorized to analyze."
            )
        if mode not in (0, 1) or isinstance(mode, bool):
            raise FaceError("Mode must be 0 (all faces) or 1 (largest face).")
        return await asyncio.to_thread(self._analyze, image_url, mode)
