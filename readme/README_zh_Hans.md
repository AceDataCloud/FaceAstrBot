# AstrBot 的 Face Transform 插件

通过自己的 Ace Data Cloud 账号，在 AstrBot 聊天中分析有处理权限的 HTTPS 图片的人脸关键点。本插件首版**仅提供 Face Analyze**；美化、年龄变化、换脸、卡通化和活体检测尚未包含。

这是 **Ace Data Cloud 提供的 Face Transform 独立集成**，不是 Face Transform 厂商或 AstrBot 团队的官方插件。请使用自己的 Ace API Key。

[English guide](../README.md) · [Face API](https://platform.acedata.cloud/documents?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=faceastrbot_readme_documents) · [当前价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=faceastrbot_readme_pricing)

## 1. 查找与安装

当前上游菜单为 **插件 → 顶部插件 → 插件市场 / 已安装**；旧英文版本可能仍写 Extensions。在插件市场搜索 **Face Transform**，核对 **Face Transform by Ace Data Cloud**、作者 **acedatacloud** 与对应服务图标。

已有 [Cloud 正式条目](https://cloud.astrbot.app/plugin/AceDataCloud/astrbot_plugin_face_acedatacloud)，当前市场版本仍为 `0.1.0`。点击 **安装** 后回到 **已安装** 检查启用和加载状态。此 PR 的 `0.1.1` 是说明/图片更新，尚未发布到 Cloud，不能把源码合并当成市场包已更新。

仓库安装：**插件 → 插件 → 已安装 → 安装插件（+）→ 从链接安装**，输入 `https://github.com/AceDataCloud/FaceAstrBot`。源码已经存在；安装后核启用和加载状态。仓库/文件安装与官方市场安装分别记账。

**访问限制：** 当前 Ace 服务目录将本服务标为私有/受限；安装插件不自动获得服务权限。仅已有对应权限的账户可使用，其他用户应先确认账户资格，不要为试用先发付费请求。此项不是服务已退役的证明。

## 2. 获取 Key 和获授权的图片

首次使用请先注册并登录；如果应用页还没有通用应用，点击 **初始化通用应用（Initialize General Application）**，再按下面步骤管理密钥。

登录 [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=faceastrbot_readme_api_key)，复制 **General application** API Key，或在 **Manage Keys → Create** 创建 AstrBot 专用 Key。服务专用 Key 必须允许 `/face/analyze`。Face Analyze 权限可能取决于账号开通情况；调用前检查当前价格和余额。

只处理自己拥有或获准处理的图片。下方示例是先前生成的虚构测试人像。图片 URL 必须是公开可访问的 HTTPS 链接；插件不会上传本地文件。只复制 Key 本身，不加 `Bearer `，也不要使用 `platform-...` 管理 Token。

### Token 图文：复制或创建专用 Key

先[注册或登录 Ace](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=faceastrbot_readme_signup)，打开 **Applications → General application**；没有通用应用时先初始化。图中 **1** 复制现有 Key，**2 Manage Keys → Create** 创建专用 Key。API 限制开启时应包含 `/face/analyze`，并检查账户当前权限、余额与价格。

![Ace 应用页复制 Key 或管理 Key（已脱敏）](../_assets/tutorial/get-api-key-en.png)

专用 Key 可命名为 `AstrBot Face Transform`；到期和限额按需设置。下图中的 `Dify tutorial` 是旧示例名称，不需要照抄。

![创建专用 API Key（共享 Ace 页面，非 AstrBot）](../_assets/tutorial/create-api-key-en.png)

两张图于 **2026-10-19** 复用核验，原拍摄日期未知，凭据/App ID/余额均已脱敏；这是共享 Ace Applications 页面，不是 AstrBot 安装或真实调用证明。[原图来源与限制](../_assets/tutorial/sources.json)。

### 在 AstrBot 填写哪里

打开 **插件 → 插件 → 已安装**，点击 **Face Transform by Ace Data Cloud** 卡片齿轮（插件配置），在 **Ace Data Cloud API key with Face Analyze access**（字段 `api_key`）粘贴 Key 并保存。只填 Key 本身，不加 `Bearer `；不填到模型提供商或聊天消息。界面遮罩不加密磁盘配置，请保护 AstrBot 数据目录。此处提供准确文字路径；不以假界面代替本插件最新设置截图。

## 3. 配置 AstrBot

在 **Plugins → Plugins → Installed** 点击 **Face Transform by Ace Data Cloud** 的齿轮，将 Key 填入 **Ace Data Cloud API key with Face Analyze access** 并保存。WebUI 会遮蔽输入，但 AstrBot 数据目录存储原值，应保护该目录。

选择支持工具调用的聊天模型，在当前 Profile 和 Persona 中允许 `face_analyze`。工具未出现时检查 **Plugins → Manage Behaviors → Function Tools**。

## 4. 在聊天中分析一次

向机器人发送：

> 使用 `face_analyze` 对这张获授权的虚构测试人像只分析一次，mode 为 `1`：`https://platform2.cdn.acedata.cloud/seedream/00355681-7e81-49a4-a8fc-d2165fe1e9fd.jpg`。告诉我图片尺寸和人脸数量。

mode `1` 分析面积最大的人脸，mode `0` 请求分析全部人脸。工具同步调用 `/face/analyze`，返回图片尺寸、人脸数量及最多三个人脸的形状数据；无需 task ID 或轮询。无可检测人脸时返回 0 也可能是正常结果。

## 5. 核对用量与排障

在 Ace Data Cloud 用量中筛选 **Face Analyze API**。若工具响应有 trace ID，可精确匹配；若没有，应用/API/时间只能作为关联线索，不能证明某一条记录。当前源码成本规则为每次分析 0.0025 Credits，账户折扣另计；使用前核对线上价格与权限。

| 现象 | 检查项 |
| --- | --- |
| 插件加载失败 | AstrBot 版本、**Failed to Load Plugins**、**Data & Logs → Logs**。 |
| 看不到工具 | 插件已启用；当前 Profile/Persona 允许工具；模型支持工具调用。 |
| HTTP 401/403 | Key 类型、有效期、余额、Face Analyze 权限及 Allowed APIs。 |
| 图片无法分析 | 图片 HTTPS 链接可访问，且你有权处理其内容。 |
| 网络失败 | 重试前查请求历史；超时请求仍可能已有用量。 |

插件只向 `https://api.acedata.cloud` 发送 Key，拒绝重定向，不自动重试付费调用。使用 Python 标准库，无新增依赖。

## 已验证的本地运行

隔离的官方 AstrBot `v4.28.2` 实例中，ChatUI 对虚构示例图片实际调用 `face_analyze` 一次，返回 2048×2048 和 1 张脸。[脱敏证据](../tests/e2e-results.json)记录本地运行结果及账单归属边界。

## 已验证的市场安装

2026-10-12，[Cloud 公开卡片](https://cloud.astrbot.app/plugin/AceDataCloud/astrbot_plugin_face_acedatacloud)显示版本 `0.1.0`。独立的全新 AstrBot `v4.28.2` 实例通过官方市场安装，读回 `install_method: market` 与 `activated: true`。ChatUI 仅对已授权的虚构人像调用一次 `face_analyze`，返回 2048×2048 图像中的一张脸。响应没有 trace ID，因此不声称精确匹配某一条账单。[脱敏市场证据](https://github.com/AceDataCloud/Index/blob/main/plans/ecosystem-growth/agent-provider-onboarding/execution/evidence/astrbot-market-20261012.json)记录安装与调用。

## 品牌素材

`logo.svg` 是未修改的当前 [Face 服务图标](https://cdn.acedata.cloud/796e72ed6c.svg)，SHA-256 `cd7e8a610a6a099c7f4037781725f8da2c08d414f9efa00094fe0c6ea136758c`；AstrBot 卡片使用的 `logo.png` 是该 SVG 的 256×256 光栅化，SHA-256 `3fe685797f640bed7bb4f741cc791673e3b518458257762c32519f606b57d575`。
