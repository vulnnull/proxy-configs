#!/usr/bin/env python3
"""
规则生成器 — 从 source/*.txt 自动生成:
  - list/*.list  (Surge/Egern/Shadowrocket 格式)
  - yaml/*.yaml  (Clash 格式)

源文件格式 (rules/source/xxx.txt):
  # 注释行
  domain.com            → DOMAIN-SUFFIX (后缀匹配)
  =exact.domain.com     → DOMAIN (精确匹配)
  ~keyword              → DOMAIN-KEYWORD
  ip:10.0.0.0/8         → IP-CIDR
  ip6:::1/128           → IP-CIDR6
"""
import os, re

SOURCE_DIR = "rules/source"
LIST_DIR = "rules/list"
YAML_DIR = "rules/yaml"
HEADER = ""

def parse_line(line: str):
    """解析一行源文件，返回 (rule_type, value) 或 None"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("ip6:"):
        return ("IP-CIDR6", line[4:])
    if line.startswith("ip:"):
        return ("IP-CIDR", line[3:])
    if line.startswith("~"):
        return ("DOMAIN-KEYWORD", line[1:])
    if line.startswith("="):
        return ("DOMAIN", line[1:])
    return ("DOMAIN-SUFFIX", line)


def generate():
    os.makedirs(LIST_DIR, exist_ok=True)
    os.makedirs(YAML_DIR, exist_ok=True)

    for fname in sorted(os.listdir(SOURCE_DIR)):
        if not fname.endswith(".txt"):
            continue
        base = fname[:-4]  # 去掉 .txt
        src_path = os.path.join(SOURCE_DIR, fname)

        with open(src_path, encoding="utf-8") as f:
            lines = f.readlines()

        list_lines = []
        yaml_payload = []

        for line in lines:
            parsed = parse_line(line)
            if parsed is None:
                continue
            rtype, value = parsed

            # list 格式: DOMAIN-SUFFIX,domain.com
            list_lines.append(f"{rtype},{value}")

            # yaml 格式: Clash 用 '- "+.xxx"' 或 '- "xxx"'
            if rtype == "DOMAIN-SUFFIX":
                yaml_payload.append(f"  - '+.{value}'")
            elif rtype == "DOMAIN":
                yaml_payload.append(f"  - '{value}'")
            elif rtype == "DOMAIN-KEYWORD":
                yaml_payload.append(f"  - '~{value}'")
            elif rtype in ("IP-CIDR", "IP-CIDR6"):
                yaml_payload.append(f"  - '{rtype},{value}'")

        # 写入 list 文件
        list_path = os.path.join(LIST_DIR, f"{base}.list")
        with open(list_path, "w", encoding="utf-8") as f:
            f.write(f"# Generated from source/{fname}\n")
            for l in list_lines:
                f.write(l + "\n")
        print(f"  ✓ list/{base}.list ({len(list_lines)} rules)")

        # 写入 yaml 文件
        yaml_path = os.path.join(YAML_DIR, f"{base}.yaml")
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(f"# Generated from source/{fname}\n")
            f.write("payload:\n")
            for p in yaml_payload:
                f.write(p + "\n")
        print(f"  ✓ yaml/{base}.yaml ({len(yaml_payload)} rules)")


if __name__ == "__main__":
    generate()
