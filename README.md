# Face Transform for AstrBot

Analyze face keypoints in an authorized HTTPS image from AstrBot chat through your own Ace Data Cloud account. This first plugin version offers **Face Analyze** only; beautification, aging, swapping, cartoon, and liveness operations are not included.

This independent **Face Transform integration is provided by Ace Data Cloud**; it is not an official plugin from the Face Transform publisher or the AstrBot team. Use your own Ace API key.

[简体中文指南](readme/README_zh_Hans.md) · [Face API](https://platform.acedata.cloud/documents?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=faceastrbot_readme_documents) · [Current prices](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=faceastrbot_readme_pricing)

## 1. Find and install

Current upstream navigation is **Plugins → Plugins → Plugin Market / Installed**; older English versions may label the section Extensions. Search **Face Transform** and verify **Face Transform by Ace Data Cloud**, author **acedatacloud**, and the matching service icon.

An [official Cloud listing](https://cloud.astrbot.app/plugin/AceDataCloud/astrbot_plugin_face_acedatacloud) exists at market version `0.1.0`. Select **Install**, then check that it is enabled without a load error under **Installed**. This PR’s `0.1.1` is a documentation/image update and is not yet a Cloud release; merging source does not update the market package.

Repository installation: **Plugins → Plugins → Installed → Install Plugin (+) → Install from URL**, with `https://github.com/AceDataCloud/FaceAstrBot`. Source is already available. Confirm it is enabled and loaded. A repository/file installation is a separate path from official market installation.

**Access restriction:** the current Ace service catalog marks this service private/restricted. Installing the plugin does not grant service entitlement. Use an already entitled account or confirm eligibility first; do not send a paid trial request just to test access. This flag alone does not mean the service is retired.

## 2. Get a key and an authorized image

New account? Register and sign in first. If the Applications page has no General application yet, choose **Initialize General Application**, then continue with the key steps below.

Sign in at [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=faceastrbot_readme_api_key). Copy the **General application** API key or use **Manage Keys → Create** to make a dedicated AstrBot key. A service-specific key must permit `/face/analyze`. Face Analyze access may depend on your account entitlement. Check current pricing and balance before running it.

Use only an image you own or have permission to process. The first-run example below uses a previously generated fictional test portrait. The URL must be public HTTPS; this plugin does not upload local files. Copy only the API key value, without `Bearer `, and do not use a `platform-...` management token.

### Token screenshots: copy or create a dedicated key

[Register or sign in to Ace](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=faceastrbot_readme_signup), then open **Applications → General application** and initialize it if absent. Use **1** to copy the selected key, or **2 Manage Keys → Create** for a dedicated key. If Allowed APIs is enabled, include `/face/analyze`; check current entitlement, balance and prices before use.

![Copy an Ace key or open Manage Keys (redacted)](_assets/tutorial/get-api-key-en.png)

Use a name such as `AstrBot Face Transform` and set expiry/limits as needed. The screenshot’s `Dify tutorial` is an older example, not a required label.

![Create an optional dedicated API key (shared Ace page, not AstrBot)](_assets/tutorial/create-api-key-en.png)

Images were reused and checked on **2026-10-19**; original capture dates are unknown. Credentials, App ID and balance are redacted. This is the shared Ace Applications UI, not proof of AstrBot installation or a live service call. [Image sources and limits](_assets/tutorial/sources.json).

### Where to paste it in AstrBot

Open **Plugins → Plugins → Installed**, select the gear (**Plugin Configuration**) on **Face Transform by Ace Data Cloud**, paste the key into **Ace Data Cloud API key with Face Analyze access** (stored field `api_key`), and save. Paste the key only, with no `Bearer ` prefix; never put it in model-provider settings or a chat prompt. UI masking does not encrypt the data-directory config. These are exact text steps; no fabricated settings image is used.

## 3. Configure AstrBot

Under **Plugins → Plugins → Installed**, select the gear icon on **Face Transform by Ace Data Cloud**. Paste the key into **Ace Data Cloud API key with Face Analyze access** and save. The dashboard masks the input, while the AstrBot data directory stores the original value; protect that directory.

Choose a chat model with tool calling and allow `face_analyze` for the active profile and persona. Check **Plugins → Manage Behaviors → Function Tools** if the tool is unavailable.

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

On an isolated official AstrBot `v4.28.2` instance, ChatUI invoked `face_analyze` once for the fictional example image and returned one face in a 2048×2048 image. [Sanitized evidence](tests/e2e-results.json) records the local runtime result and its billing attribution limit.

## Verified market installation

On 2026-10-12, the public [Cloud listing](https://cloud.astrbot.app/plugin/AceDataCloud/astrbot_plugin_face_acedatacloud) reported version `0.1.0`. A separate clean AstrBot `v4.28.2` instance installed the package through the official market and read back `install_method: market` and `activated: true`. ChatUI called `face_analyze` once on an authorized fictional portrait and returned one face at 2048×2048. The response contained no trace ID, so an exact billing-row match is not claimed. [Sanitized market evidence](https://github.com/AceDataCloud/Index/blob/main/plans/ecosystem-growth/agent-provider-onboarding/execution/evidence/astrbot-market-20261012.json) records the installation and call.

## Brand asset

`logo.svg` is the unmodified current [Face service icon](https://cdn.acedata.cloud/796e72ed6c.svg), SHA-256 `cd7e8a610a6a099c7f4037781725f8da2c08d414f9efa00094fe0c6ea136758c`. `logo.png` is a 256×256 rasterization of that SVG for AstrBot's plugin card, SHA-256 `3fe685797f640bed7bb4f741cc791673e3b518458257762c32519f606b57d575`.
