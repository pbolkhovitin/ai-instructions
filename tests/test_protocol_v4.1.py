#!/usr/bin/env python3
import json, os, sys, glob, re
from pathlib import Path

BASE = Path(__file__).parent.parent
V4_DIR = BASE / "instructions" / "deepseek_v4"
EXPECTED_VERSION = "4.1.0"

errors = []
warnings = []

def err(msg):
    errors.append(msg)

def warn(msg):
    warnings.append(msg)

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def check(cond, msg):
    if not cond:
        err(msg)

# ------- 1. All JSON files valid syntax -------
json_files = list(V4_DIR.glob("*.json"))
check(len(json_files) > 0, f"No JSON files found in {V4_DIR}")
for p in json_files:
    try:
        load_json(p)
    except json.JSONDecodeError as e:
        err(f"Invalid JSON in {p.name}: {e}")

# ------- 2. Version sync (v4.1.0 files only, skip legacy) -------
for p in json_files:
    if "_v4.0" in p.name or p.name == "version_manifest_v4.1.0.json":
        continue
    try:
        data = load_json(p)
        v = data.get("version") or data.get("protocol")
        if v != EXPECTED_VERSION:
            err(f"{p.name}: version={v}, expected {EXPECTED_VERSION}")
    except:
        pass

# manifest has different structure
manifest = load_json(V4_DIR / "version_manifest_v4.1.0.json")
check(manifest.get("protocol_version") == EXPECTED_VERSION,
      f"manifest protocol_version={manifest.get('protocol_version')}")

# ------- 3. Verify all module files referenced exist -------
core = load_json(V4_DIR / "core_protocol_v4.1.0.json")
avail = core.get("content", {}).get("module_system", {}).get("available_modules", {})
for key, mod in avail.items():
    fname = mod.get("file")
    if fname:
        check((V4_DIR / fname).exists(),
              f"Module '{key}' references missing file: {fname}")
    mv = mod.get("version")
    check(mv == EXPECTED_VERSION,
          f"Module '{key}': version={mv}, expected {EXPECTED_VERSION}")
    mc_min = mod.get("min_core_version")
    mc_max = mod.get("max_core_version")
    check(mc_min == EXPECTED_VERSION,
          f"Module '{key}': min_core_version={mc_min}")
    check(mc_max is not None,
          f"Module '{key}': missing max_core_version")
    mod_url = mod.get("url", "")
    check(mod_url.startswith("https://raw.githubusercontent.com/"),
          f"Module '{key}': url missing or invalid: {mod_url}")
    check(mod_url.endswith(mod.get("file", "")),
          f"Module '{key}': url doesn't end with filename")

# ------- 4. Core protocol required fields -------
check("protocol_version" in core, "root.protocol_version missing")
check("url" in core, "root.url missing")
check(core["url"].startswith("https://raw.githubusercontent.com/"),
      f"root.url invalid: {core.get('url')}")
check(core.get("version") == EXPECTED_VERSION, f"root.version={core.get('version')}")
check(core.get("protocol") == EXPECTED_VERSION, f"root.protocol={core.get('protocol')}")

# persona_system
ps = core.get("persona_system", {})
check(ps.get("enabled") == True, "persona_system.enabled != true")
check(ps.get("version") == EXPECTED_VERSION, f"persona_system.version={ps.get('version')}")
check(ps.get("default_persona") == "C",
      f"default_persona={ps.get('default_persona')}, expected C")
check(ps.get("auto_detect", {}).get("enabled") == False,
      "auto_detect.enabled != false")

# content.core_only_mode
com = core.get("content", {}).get("core_only_mode", {})
check(com.get("show_welcome_on_load") == True, "show_welcome_on_load != true")
check(com.get("hide_protocol_body") == True, "hide_protocol_body != true")
wm = com.get("welcome_message", "")
check(len(wm) > 0, "welcome_message is empty")
check("{" not in wm, "welcome_message contains JSON body")
check("core_protocol_v4" not in wm, "welcome_message references protocol filename")

# version_check
vc = core.get("version_check", {})
check(vc.get("enabled") == True, "version_check.enabled != true")
check(vc.get("mode") == "strict", f"version_check.mode={vc.get('mode')}")

# protocol_commands
pc = core.get("content", {}).get("protocol_commands", {}).get("[ПРОТОКОЛ: ЗАГРУЗИТЬ URL]", {})
check(pc.get("required_params") == [],
      f"protocol_command required_params={pc.get('required_params')} (should be empty, default persona=C)")

# ------- 5. think_pipeline in available_modules -------
check("think_pipeline" in avail, "think_pipeline not in available_modules")

# ------- 6. auto_load_strategy includes think_pipeline ----
als = core.get("content", {}).get("module_system", {}).get("auto_load_strategy", {})
check("think_pipeline" in als.get("critical_modules", []),
      "think_pipeline not in auto_load_strategy.critical_modules")

# ------- 7. Version manifest consistency -------
manifest_comps = manifest.get("components", {})
# check top-level entries (core, think_pipeline)
for comp_name in ("core", "think_pipeline"):
    comp_data = manifest_comps.get(comp_name, {})
    cv = comp_data.get("version")
    check(cv == EXPECTED_VERSION,
          f"Manifest '{comp_name}': version={cv}")
# check modules sub-object
mods = manifest_comps.get("modules", {})
for mod_name, mod_data in mods.items():
    cv = mod_data.get("version")
    check(cv == EXPECTED_VERSION,
          f"Manifest module '{mod_name}': version={cv}")
    mc = mod_data.get("min_core") or mod_data.get("min_core_version")
    check(mc == EXPECTED_VERSION,
          f"Manifest module '{mod_name}': min_core={mc}")

# ------- 8. Check base_repo_url format ----
repo_url = core.get("content", {}).get("module_system", {}).get("base_repo_url", "")
check(repo_url.startswith("https://raw.githubusercontent.com/"),
      f"base_repo_url format suspicious: {repo_url}")

# verify it resolves to a real owner
url_match = re.match(r"https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/", repo_url)
check(url_match is not None, f"base_repo_url pattern mismatch: {repo_url}")
if url_match:
    owner, repo = url_match.group(1), url_match.group(2)
    check(owner == "pbolkhovitin", f"base_repo_url owner={owner}, expected pbolkhovitin")

# ------- 9. All v4.1.0 module files contain min/max_core_version -------
for p in json_files:
    if "_v4.0" in p.name or p.name in ("core_protocol_v4.1.0.json", "version_manifest_v4.1.0.json"):
        continue
    try:
        data = load_json(p)
        check(data.get("min_core_version") == EXPECTED_VERSION,
              f"{p.name}: min_core_version={data.get('min_core_version')}")
        check(data.get("max_core_version") is not None,
              f"{p.name}: max_core_version missing")
    except:
        pass

# ------- RESULTS -------
def main():
    print(f"Validating {len(json_files)} JSON files in {V4_DIR}")
    print()
    passed = len(errors) == 0
    for e in errors:
        print(f"  FAIL  {e}")
    for w in warnings:
        print(f"  WARN  {w}")

    print()
    print(f"Errors: {len(errors)}, Warnings: {len(warnings)}")
    if passed:
        print("PASSED")
    else:
        print("FAILED")
    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
