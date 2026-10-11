"""Face Transform keypoint tool for AstrBot."""

from __future__ import annotations

import json

from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

from .client import FaceAnalyzeClient, FaceError


class FacePlugin(Star):
    """Analyze facial keypoints from an authorized image in chat."""

    def __init__(self, context: Context, config: AstrBotConfig) -> None:
        """Receive the key from AstrBot's plugin configuration.

        Args:
            context: AstrBot plugin context.
            config: Configuration with a masked Ace Data Cloud key.
        """
        super().__init__(context)
        self.config = config

    @filter.llm_tool(name="face_analyze")
    async def face_analyze(
        self, event: AstrMessageEvent, image_url: str, mode: int = 1
    ) -> str:
        """Analyze face landmarks in an HTTPS image the user may process.

        Args:
            image_url(string): Authorized HTTPS portrait image URL.
            mode(number): 1 analyzes the largest face; 0 analyzes all faces.

        Returns:
            JSON dimensions, face count, and keypoint data for up to three faces.
        """
        try:
            result = await FaceAnalyzeClient(self.config.get("api_key", "")).analyze(
                image_url, mode
            )
        except FaceError as exc:
            result = {"status": "error", "message": str(exc)}
        return json.dumps(result, ensure_ascii=False)
