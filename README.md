# Proxy Configs

代理工具配置合集，统一维护规则，同时支持 **Egern** / **Shadowrocket** / **Clash**。

## 目录结构

```
proxy-configs/
├── rules/                    ← 规则中心
│   ├── source/               ← 📝 源文件（你只需维护这一份）
│   │   ├── AI.txt            # AI 服务域名
│   │   ├── Apple.txt         # Apple 服务域名
│   │   ├── ApplePush.txt     # Apple 推送域名
│   │   ├── Google.txt        # Google 服务域名
│   │   ├── PrivateDirect.txt # 私人直连域名
│   │   └── PrivateProxy.txt  # 私人代理域名
│   ├── list/                 ← ⚙️ 自动生成 → Egern / Shadowrocket 引用
│   └── yaml/                 ← ⚙️ 自动生成 → Clash 引用
├── egern/
│   ├── egern.yaml            # Egern 主配置
│   ├── Rule/                 # Egern 原生 YAML 规则
│   ├── Module/               # 功能模块（含 Sub-Store）
│   └── Widget/               # 桌面小组件
├── sr-rules/
│   ├── sr.conf               # Shadowrocket 主配置（含 Sub-Store 面板）
│   ├── rule/                 # SR 特有规则（GitLab / China / Global / Atlassian）
│   └── qr.png
├── clash/
│   └── config.yaml           # Clash 主配置
└── scripts/
    └── generate.py           # 生成器：source/ → list/ + yaml/
```

## 工作流

```
编辑 source/*.txt  ──→  generate.py  ──→  list/*.list（Surge 格式）
                    │                    └──  yaml/*.yaml（Clash 格式）
                    │
GitHub Action（每周一四自动同步上游 blackmatrix7）
```

## 维护规则

只需编辑 `rules/source/*.txt`，每行一个域名：

```
# rules/source/PrivateProxy.txt
minimaxi.com
minimax.chat
bigmodel.cn
z.ai
```

**源文件格式：**

| 写法 | 含义 | 生成规则 |
|------|------|---------|
| `domain.com` | 后缀匹配（默认） | `DOMAIN-SUFFIX,domain.com` |
| `=domain.com` | 精确匹配 | `DOMAIN,domain.com` |
| `~keyword` | 关键词匹配 | `DOMAIN-KEYWORD,keyword` |
| `ip:x.x.x.x/y` | IP 段匹配 | `IP-CIDR,x.x.x.x/y` |
| `ip6:xx::/yy` | IPv6 段匹配 | `IP-CIDR6,xx::/yy` |

## 使用方式

| 工具 | URL |
|------|------|
| **Egern** | `https://raw.githubusercontent.com/vulnnull/proxy-configs/main/egern/egern.yaml` |
| **Shadowrocket** | `https://raw.githubusercontent.com/vulnnull/proxy-configs/main/sr-rules/sr.conf` |
| **Clash** | `https://raw.githubusercontent.com/vulnnull/proxy-configs/main/clash/config.yaml`（需填入订阅链接） |
