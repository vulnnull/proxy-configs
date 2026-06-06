# Egern 配置

> 基于 [jnlaoshu/MySelf](https://github.com/jnlaoshu/MySelf/tree/main/Egern) 修改，集成项目统一规则体系。
>
> Egern 是一款新生代网络代理工具，详见 [Egern 官方文档](https://egernapp.com/zh-CN/docs/intro)。

## 使用方式

在 Egern 中引用以下配置链接：

```
https://raw.githubusercontent.com/vulnnull/proxy-configs/main/egern/egern.yaml
```

## 规则来源

| 来源 | 规则 | 位置 |
|------|------|------|
| 🔧 **自维护** | 私人直连 / 私人代理 / AI / Apple / Google | `rules/source/*.txt` |
| 🔄 **上游同步** | YouTube / Netflix / Disney / 媒体服务等 | `rules/list/*.list`（blackmatrix7） |
| 📄 **Egern 原生** | Lan / AdBlock / AIGC 等（YAML 格式） | `egern/Rule/*.yaml` |

## 自定义规则

编辑项目根目录 `rules/source/` 下的 `.txt` 文件即可，推送后重新加载配置自动生效：

- `rules/source/custom-direct.txt` — 私人直连
- `rules/source/custom-proxy.txt` — 私人代理
- `rules/source/AI.txt` — AI 服务
- `rules/source/Apple.txt` — Apple 服务

## 功能模块

| 模块 | 说明 |
|------|------|
| 常用小组件 | 桌面 Widget 合集 |
| Sub-Store | 订阅管理面板（自动启用） |
| WeatherKit | 天气增强模块 |
