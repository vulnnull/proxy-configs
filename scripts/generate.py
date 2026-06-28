#!/usr/bin/env python3
"""
规则生成器 — 从 source/*.txt 自动生成:
  - list/*.list         (Surge/Egern list 格式)
  - yaml/*.yaml         (Clash rule-provider 格式)
  - egern/Rule/*.yaml   (Egern 原生格式)

源文件格式 (rules/source/xxx.txt):
  # 注释行
  domain.com            → DOMAIN-SUFFIX (后缀匹配)
  =exact.domain.com     → DOMAIN (精确匹配)
  ~keyword              → DOMAIN-KEYWORD
  ua:UserAgent*         → USER-AGENT
  ip:10.0.0.0/8         → IP-CIDR
  ip6:::1/128           → IP-CIDR6
  asn:12345             → IP-ASN
  proc:ProcessName      → PROCESS-NAME
"""
import os

SOURCE_DIR = "rules/source"
LIST_DIR = "rules/list"
YAML_DIR = "rules/yaml"
EGERN_RULE_DIR = "egern/Rule"

PREFIX_MAP = {
    "ip6:": "IP-CIDR6",
    "ip:": "IP-CIDR",
    "ua:": "USER-AGENT",
    "asn:": "IP-ASN",
    "proc:": "PROCESS-NAME",
}


def parse_line(line: str):
    """解析一行源文件，返回 (rule_type, value) 或 None"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    for prefix, rtype in PREFIX_MAP.items():
        if line.startswith(prefix):
            return (rtype, line[len(prefix):])
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
        base = fname[:-4]
        src_path = os.path.join(SOURCE_DIR, fname)

        with open(src_path, encoding="utf-8") as f:
            lines = f.readlines()

        list_lines = []
        yaml_payload = []
        # Egern native buckets
        egern_domain = []
        egern_suffix = []
        egern_keyword = []
        egern_ip_cidr = []
        egern_ip_cidr6 = []
        egern_asn = []

        for line in lines:
            parsed = parse_line(line)
            if parsed is None:
                continue
            rtype, value = parsed

            # ── list 格式 (Surge/Egern/Shadowrocket) ──
            list_lines.append(f"{rtype},{value}")

            # ── yaml 格式 (Clash rule-provider) ──
            if rtype == "DOMAIN-SUFFIX":
                yaml_payload.append(f"  - '+.{value}'")
            elif rtype == "DOMAIN":
                yaml_payload.append(f"  - '{value}'")
            elif rtype == "DOMAIN-KEYWORD":
                yaml_payload.append(f"  - '~{value}'")
            elif rtype in ("IP-CIDR", "IP-CIDR6", "IP-ASN", "PROCESS-NAME"):
                yaml_payload.append(f"  - '{rtype},{value}'")

            # ── Egern 原生 yaml ──
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
            elif rtype == "IP-ASN":
                egern_asn.append(f"  - {value}")

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
        buckets = [
            ("domain_set", egern_domain),
            ("domain_suffix_set", egern_suffix),
            ("domain_keyword_set", egern_keyword),
            ("ip_cidr_set", egern_ip_cidr),
            ("ip_cidr6_set", egern_ip_cidr6),
            ("asn_set", egern_asn),
        ]
        total = sum(len(b[1]) for b in buckets)
        with open(egern_path, "w", encoding="utf-8") as f:
            f.write(f"# Generated from source/{fname}\n")
            f.write(f"# Total: {total} rules\n\n")
            for section, items in buckets:
                if items:
                    f.write(f"{section}:\n")
                    for d in items:
                        f.write(d + "\n")
                    f.write("\n")
        print(f"  ✓ egern/Rule/{base}.yaml ({total} rules)")


if __name__ == "__main__":
    generate()
