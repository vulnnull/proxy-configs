# Shadowrocket 配置

> 集成 [proxy-configs](https://github.com/vulnnull/proxy-configs) 统一规则体系。
>
> Shadowrocket 是一款 iOS 网络代理工具，支持 Surge 格式规则集。

## 使用方式

**1. 复制配置链接**

```
https://raw.githubusercontent.com/vulnnull/proxy-configs/main/sr-rules/sr.conf
```

**2. 导入 Shadowrocket**

```
Shadowrocket → 配置 → 右上角 ➕ → 粘贴链接 → 下载
```

**3. 添加节点**

首页 → 添加节点或订阅 → 连通性测试 → 选择可用节点

## 规则来源

| 来源 | 规则 | 位置 |
|------|------|------|
| 🔧 **自维护** | 私人直连 / 私人代理 / AI / Apple / Google | `rules/source/*.txt` |
| 🔄 **上游同步** | YouTube / GitHub / Telegram / 微软等 | `rules/list/*.list`（blackmatrix7） |
| 🔄 **SR 特有** | GitLab / China / Global / Atlassian | `sr-rules/rule/*.list`（blackmatrix7） |

## 自定义规则

编辑项目根目录 `rules/source/` 下的 `.txt` 文件即可，推送后 Shadowrocket 自动拉取更新。

## Sub-Store 集成

本配置已集成 Sub-Store 支持：

1. [部署 Sub-Store 后端](https://github.com/sub-store-org/Sub-Store)
2. 在 Shadowrocket 中访问 `http://sub.store` 即可打开管理面板
3. 面板脚本和跳转规则已在配置中预置

## 默认策略

| 服务 | 默认策略 |
|------|---------|
| 🤖 AI 服务 | 🇺🇸 美国节点 |
| 🔍 谷歌服务 | 🇯🇵 日本节点 |
| 📹 油管视频 | 🚀 节点选择 |
| 🍏 苹果服务 | DIRECT |
| 🐟 漏网之鱼（兜底） | 🇯🇵 日本节点 |
