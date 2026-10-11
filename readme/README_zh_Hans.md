# AstrBot 的 Face Transform 插件

通过自己的 Ace Data Cloud 账号，在 AstrBot 聊天中分析有处理权限的 HTTPS 图片的人脸关键点。本插件首版**仅提供 Face Analyze**；美化、年龄变化、换脸、卡通化和活体检测尚未包含。

[English guide](../README.md) · [Face API](https://platform.acedata.cloud/documents) · [当前价格](https://platform.acedata.cloud/models)

## 1. 搜索并安装

在 AstrBot WebUI 打开 **Extensions → Plugins → AstrBot Plugin Market**，搜索 **Face Transform**。核对卡片 **Face Transform by Ace Data Cloud**、作者 **acedatacloud** 和当前 Face 服务图标，点击 **Install**，随后到 **Installed** 确认插件已启用且没有加载错误。

AstrBot Cloud 尚未正式上架。源码合并发布后，可在 **Installed → Install (+) → Install from URL** 填入 `https://github.com/AceDataCloud/FaceAstrBot` 预览。URL 安装与官方市场搜索、安装是不同验收项。

## 2. 获取 Key 和获授权的图片

登录 [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications)，复制 **General application** API Key，或在 **Manage Keys → Create** 创建 AstrBot 专用 Key。服务专用 Key 必须允许 `/face/analyze`。Face Analyze 权限可能取决于账号开通情况；调用前检查当前价格和余额。

只处理自己拥有或获准处理的图片。下方示例是先前生成的虚构测试人像。图片 URL 必须是公开可访问的 HTTPS 链接；插件不会上传本地文件。只复制 Key 本身，不加 `Bearer `，也不要使用 `platform-...` 管理 Token。

## 3. 配置 AstrBot

在 **Extensions → Plugins → Installed** 点击 **Face Transform by Ace Data Cloud** 的齿轮，将 Key 填入 **Ace Data Cloud API key with Face Analyze access** 并保存。WebUI 会遮蔽输入，但 AstrBot 数据目录存储原值，应保护该目录。

选择支持工具调用的聊天模型，在当前 Profile 和 Persona 中允许 `face_analyze`。工具未出现时检查 **Extensions → Handlers**。

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

隔离的官方 AstrBot `v4.28.2` 实例中，ChatUI 对虚构示例图片实际调用 `face_analyze` 一次，返回 2048×2048 和 1 张脸。[脱敏证据](../tests/e2e-results.json)记录本地运行结果及账单归属边界。官方市场搜索和安装尚未验证。

## 品牌素材

`logo.svg` 是未修改的当前 [Face 服务图标](https://cdn.acedata.cloud/796e72ed6c.svg)，SHA-256 `cd7e8a610a6a099c7f4037781725f8da2c08d414f9efa00094fe0c6ea136758c`；AstrBot 卡片使用的 `logo.png` 是该 SVG 的 256×256 光栅化，SHA-256 `3fe685797f640bed7bb4f741cc791673e3b518458257762c32519f606b57d575`。
