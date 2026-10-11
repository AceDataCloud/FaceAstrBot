# Face Transform for AstrBot

Analyze face keypoints in an authorized HTTPS image from AstrBot chat through your own Ace Data Cloud account. This first plugin version offers **Face Analyze** only; beautification, aging, swapping, cartoon, and liveness operations are not included.

[简体中文指南](readme/README_zh_Hans.md) · [Face API](https://platform.acedata.cloud/documents) · [Current prices](https://platform.acedata.cloud/models)

## 1. Find and install

In AstrBot WebUI, open **Extensions → Plugins → AstrBot Plugin Market** and search **Face Transform**. Check for **Face Transform by Ace Data Cloud**, author **acedatacloud**, and the Face service icon. Choose **Install**, then verify it is enabled without a load error under **Installed**.

The AstrBot Cloud listing has not yet been published. After the source release is merged, **Installed → Install (+) → Install from URL** with `https://github.com/AceDataCloud/FaceAstrBot` offers a preview. URL installation is separate from official market discovery and installation.

## 2. Get a key and an authorized image

Sign in at [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications). Copy the **General application** API key or use **Manage Keys → Create** to make a dedicated AstrBot key. A service-specific key must permit `/face/analyze`. Face Analyze access may depend on your account entitlement. Check current pricing and balance before running it.

Use only an image you own or have permission to process. The first-run example below uses a previously generated fictional test portrait. The URL must be public HTTPS; this plugin does not upload local files. Copy only the API key value, without `Bearer `, and do not use a `platform-...` management token.

## 3. Configure AstrBot

Under **Extensions → Plugins → Installed**, select the gear icon on **Face Transform by Ace Data Cloud**. Paste the key into **Ace Data Cloud API key with Face Analyze access** and save. The dashboard masks the input, while the AstrBot data directory stores the original value; protect that directory.

Choose a chat model with tool calling and allow `face_analyze` for the active profile and persona. Check **Extensions → Handlers** if the tool is unavailable.

## 4. Analyze once in chat

Ask the bot:

> Use `face_analyze` exactly once with mode `1` for this authorized fictional portrait: `https://platform2.cdn.acedata.cloud/seedream/00355681-7e81-49a4-a8fc-d2165fe1e9fd.jpg`. Tell me the image dimensions and face count.

Mode `1` analyzes the largest face; mode `0` asks the service to analyze all faces. The tool calls `/face/analyze` synchronously and returns image dimensions, face count, and up to three shape entries. No task ID or polling is needed. A URL with no detectable face may validly return zero faces.

## 5. Check usage and troubleshoot

Filter your Ace Data Cloud usage history to **Face Analyze API**. If the tool response includes a trace ID, match it exactly. If not, application/API/time is only a correlation clue, not proof of a particular usage row. The current source cost rule is 0.0025 Credits per analysis before any account discount; verify the live price and entitlement before use.

| Symptom | Check |
| --- | --- |
| Plugin fails to load | AstrBot version, **Failed to Load Plugins**, then **Data & Logs → Logs**. |
| Tool does not appear | Plugin enabled; active profile and persona permit it; chat model supports tool calling. |
| HTTP 401 or 403 | Key type, expiry, balance, Face Analyze entitlement, and any Allowed APIs restriction. |
| Image cannot be analyzed | The image URL is reachable via HTTPS and you may process its content. |
| Network failure | Check request history before repeating a call; a timed-out response may still have usage. |

The plugin sends the key only to `https://api.acedata.cloud`, rejects redirects, and makes no automatic paid retry. It uses Python's standard library and needs no extra package.

## Verified local run

On an isolated official AstrBot `v4.28.2` instance, ChatUI invoked `face_analyze` once for the fictional example image and returned one face in a 2048×2048 image. [Sanitized evidence](tests/e2e-results.json) records the local runtime result and its billing attribution limit. Public market discovery and install remain unverified.

## Brand asset

`logo.svg` is the unmodified current [Face service icon](https://cdn.acedata.cloud/796e72ed6c.svg), SHA-256 `cd7e8a610a6a099c7f4037781725f8da2c08d414f9efa00094fe0c6ea136758c`. `logo.png` is a 256×256 rasterization of that SVG for AstrBot's plugin card, SHA-256 `3fe685797f640bed7bb4f741cc791673e3b518458257762c32519f606b57d575`.
