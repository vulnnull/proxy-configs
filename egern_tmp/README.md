# Egern 自用配置

> 基于 [jnlaoshu/MySelf](https://github.com/jnlaoshu/MySelf/tree/main/Egern) 修改的自用配置。
>
> Egern 是一款新生代网络代理工具，详见 [Egern 官方文档](https://egernapp.com/zh-CN/docs/intro)。

## 使用方式

在 Egern 中引用以下配置链接：

```
https://git.transnull.cn/transnull/Egern/raw/branch/main/egern.yaml
```

## 目录结构

```
├── egern.yaml          # 主配置文件
├── Rule/               # 路由规则
│   ├── PrivateDirect.list   # 私人直连规则
│   ├── PrivateProxy.list    # 私人代理规则
│   └── ...
├── Module/             # 功能模块
└── Widget/             # 小组件
```

## 自定义规则

- **私人直连** — 编辑 [Rule/PrivateDirect.list](Rule/PrivateDirect.list)，添加不需代理的域名
- **私人代理** — 编辑 [Rule/PrivateProxy.list](Rule/PrivateProxy.list)，添加需要走代理的域名
