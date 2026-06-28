#!/usr/bin/env python3
"""
规则生成器 — 从 source/*.txt 自动生成:
  - list/*.list         (Surge/Egern list 格式)
  - yaml/*.yaml         (Clash rule-provider 格式)
  - egern/Rule/*.yaml   (Egern 原生 domain_set 格式)

源文件格式 (rules/source/xxx.txt):
  # 注释行
  domain.com            → DOMAIN-SUFFIX (后缀匹配)
  =exact.domain.com     → DOMAIN (精确匹配)
  ~keyword              → DOMAIN-KEYWORD
  ua:UserAgent*         → USER-AGENT (仅 list 格式，Clash/Egern native 不支持)
  ip:10.0.0.0/8         → IP-CIDR
  ip6:::1/128           → IP-CIDR6
"""
import os

SOURCE_DIR = "rules/source"
LIST_DIR = "rules/list"
YAML_DIR = "rules/yaml"
EGERN_RULE_DIR = "egern/Rule"


def parse_line(line: str):
    """解析一行源文件，返回 (rule_type, value) 或 None"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("ip6:"):
        return ("IP-CIDR6", line[4:])
    if line.startswith("ip:"):
        return ("IP-CIDR", line[3:])
    if line.startswith("ua:"):
        return ("USER-AGENT", line[3:])
    if line.startswith("~"):
        return ("DOMAIN-KEYWORD", line[1:])
    if line.startswith("="):
        return ("DOMAIN", line[1:])
    return ("DOMAIN-SUFFIX", line)


def generate():
    os.makedirs(LIST_DIR, exist_ok=True)
    os.makedirs(YAML_DIR, exist_ok=True)
    os.makedirs(EGERN_RULE_DIR, exist_ok=True)

    for fname in sorted(os.listdir(SOURCE_DIR)):
        if not fname.endswith(".txt"):
            continue
        base = fname[:-4]  # 去掉 .txt
        src_path = os.path.join(SOURCE_DIR, fname)

        with open(src_path, encoding="utf-8") as f:
            lines = f.readlines()

        list_lines = []
        yaml_payload = []
        egern_domain = []
        egern_suffix = []
        egern_keyword = []
        egern_ip_cidr = []
        egern_ip_cidr6 = []

        for line in lines:
            parsed = parse_line(line)
            if parsed is None:
                continue
            rtype, value = parsed

            # ── list 格式 (Surge/Egern/Shadowrocket) ──
            list_lines.append(f"{rtype},{value}")

            # ── yaml 格式 (Clash rule-provider) ──
            # 注意: USER-AGENT 在 Clash classical rule-provider 中无效，跳过
            if rtype == "DOMAIN-SUFFIX":
                yaml_payload.append(f"  - '+.{value}'")
            elif rtype == "DOMAIN":
                yaml_payload.append(f"  - '{value}'")
            elif rtype == "DOMAIN-KEYWORD":
                yaml_payload.append(f"  - '~{value}'")
            elif rtype in ("IP-CIDR", "IP-CIDR6"):
                yaml_payload.append(f"  - '{rtype},{value}'")

            # ── Egern 原生 yaml 格式 (domain_set/suffix_set…) ──
            # USER-AGENT 在 Egern 原生格式中不支持，跳过
            if rtype == "DOMAIN":
                egern_domain.append(f"  - {value}")
            elif rtype == "DOMAIN-SUFFIX":
                egern_suffix.append(f"  - {value}")
            elif rtype == "DOMAIN-KEYWORD":
                egern_keyword.append(f"  - {value}")
            elif rtype == "IP-CIDR":
                egern_ip_cidr.append(f"  - '{value}'")
            elif rtype == "IP-CIDR6":
                egern_ip_cidr6.append(f"  - '{value}'")

        # ── 写入 list 文件 ──
        list_path = os.path.join(LIST_DIR, f"{base}.list")
        with open(list_path, "w", encoding="utf-8") as f:
            f.write(f"# Generated from source/{fname}\n")
            for l in list_lines:
                f.write(l + "\n")
        print(f"  ✓ list/{base}.list ({len(list_lines)} rules)")

        # ── 写入 Clash yaml ──
        yaml_path = os.path.join(YAML_DIR, f"{base}.yaml")
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(f"# Generated from source/{fname}\n")
            f.write("payload:\n")
            for p in yaml_payload:
                f.write(p + "\n")
        print(f"  ✓ yaml/{base}.yaml ({len(yaml_payload)} rules)")

        # ── 写入 Egern 原生 yaml ──
        egern_path = os.path.join(EGERN_RULE_DIR, f"{base}.yaml")
        total = len(egern_domain) + len(egern_suffix) + len(egern_keyword) + len(egern_ip_cidr) + len(egern_ip_cidr6)
        with open(egern_path, "w", encoding="utf-8") as f:
            f.write(f"# Generated from source/{fname}\n")
            f.write(f"# Total: {total} rules\n\n")
            if egern_domain:
                f.write("domain_set:\n")
                for d in egern_domain:
                    f.write(d + "\n")
                f.write("\n")
            if egern_suffix:
                f.write("domain_suffix_set:\n")
                for d in egern_suffix:
                    f.write(d + "\n")
                f.write("\n")
            if egern_keyword:
                f.write("domain_keyword_set:\n")
                for d in egern_keyword:
                    f.write(d + "\n")
                f.write("\n")
            if egern_ip_cidr:
                f.write("ip_cidr_set:\n")
                for d in egern_ip_cidr:
                    f.write(d + "\n")
                f.write("\n")
            if egern_ip_cidr6:
                f.write("ip_cidr6_set:\n")
                for d in egern_ip_cidr6:
                    f.write(d + "\n")
                f.write("\n")
        print(f"  ✓ egern/Rule/{base}.yaml ({total} rules)")


if __name__ == "__main__":
    generate()
