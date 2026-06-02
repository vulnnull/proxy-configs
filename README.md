# Proxy Configs

代理工具配置合集，统一维护通用规则，同时支持 **Egern** 和 **Shadowrocket**。

## 目录结构

```
proxy/
├── rules/                  ← 通用规则（Surge 格式 .list，双软件通用）
│   ├── AI.list             # AI 服务（ChatGPT、Claude 等）
│   ├── Apple.list          # Apple 服务
│   ├── ApplePush.list      # Apple 推送
│   ├── Google.list         # Google 服务
│   ├── PrivateDirect.list  # 私人直连
│   └── PrivateProxy.list   # 私人代理
├── Egern/                  ← Egern 配置
│   ├── egern.yaml          # 主配置
│   ├── Rule/               # Egern 原生 YAML 规则
│   ├── Module/             # 功能模块
│   └── Widget/             # 小组件
└── sr-rules/               ← Shadowrocket 配置
    ├── sr.conf             # 主配置
    └── ...
```

## 使用方式

### Egern

```
https://raw.githubusercontent.com/vulnnull/proxy/main/Egern/egern.yaml
```

### Shadowrocket

```
https://raw.githubusercontent.com/vulnnull/proxy/main/sr-rules/sr.conf
```

## 维护通用规则

编辑 `rules/` 下的 `.list` 文件即可同时对两个软件生效：

- `PrivateDirect.list` — 自定直连域名
- `PrivateProxy.list` — 自定代理域名
- `AI.list` — AI 服务域名
- `Apple.list` — Apple 服务域名
- 等等（可自行扩展）
