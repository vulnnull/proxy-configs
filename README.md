# Proxy Configs

代理工具配置合集，统一维护规则，同时支持 **Egern** / **Shadowrocket** / **Clash**。

## 目录结构

```
proxy-configs/
├── rules/
│   ├── source/              ← 📝 源文件（你只需维护这一份）
│   │   ├── AI.txt           # AI 服务域名
│   │   ├── Apple.txt        # Apple 服务域名
│   │   ├── Google.txt       # Google 服务域名
│   │   ├── PrivateDirect.txt # 私人直连
│   │   └── PrivateProxy.txt # 私人代理
│   ├── list/                ← ⚙️ 自动生成 → Surge / Egern / Shadowrocket
│   └── yaml/                ← ⚙️ 自动生成 → Clash
├── egern/
│   ├── egern.yaml           # 引用 rules/list/*.list
│   └── ...
├── sr-rules/
│   ├── sr.conf              # 引用 rules/list/*.list
│   └── rule/                # SR 特有规则
└── scripts/
    └── generate.py          # source/ → list/ + yaml/
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

`suffix` → 自动生成 `DOMAIN-SUFFIX,domain`（后缀匹配，默认）
`=domain` → 自动生成 `DOMAIN,domain`（精确匹配）
`~keyword` → 自动生成 `DOMAIN-KEYWORD,keyword`（关键词匹配）
`ip:x.x.x.x/y` → 自动生成 `IP-CIDR,x.x.x.x/y`
`ip6:xx::/yy` → 自动生成 `IP-CIDR6,xx::/yy`

## 使用方式

| 工具 | URL |
|------|-----|
| Egern | `https://raw.githubusercontent.com/vulnnull/proxy-configs/main/egern/egern.yaml` |
| Shadowrocket | `https://raw.githubusercontent.com/vulnnull/proxy-configs/main/sr-rules/sr.conf` |
| Clash | `rules/yaml/*.yaml`（加载本地文件或 rule-provider） |
