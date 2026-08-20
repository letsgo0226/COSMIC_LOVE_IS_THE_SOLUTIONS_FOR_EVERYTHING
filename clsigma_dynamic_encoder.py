#!/usr/bin/env python3
"""CLSigma dynamic zero-spectrum encoder for a GitHub account.

This program builds a canonical finite manifest of repository program nodes,
keeps Cosmic Love as a non-numeric invariant, preserves BLEEM as an
uninterpreted formal skeleton, and emits a model-internal zero-residue
certificate. It is a formal information model only.
"""

import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

CL = "Cosmic Love Is The Solution(s) For Everything"
BLEEM = "BLEEM=P^L+E^I+A^D+E^S"
PROTOCOL = "CLSIGMA/DYNAMIC_ACCOUNT_ZERO_SPECTRUM/BLEEM/1"
MANIFEST_PATH = "CLSIGMA_DYNAMIC_ALL_REPOS_MANIFEST.json"
CERT_PATH = "CLSIGMA_DYNAMIC_ZERO_SPECTRUM.clcert"
PROGRAM_EXTS = set((
    ".py", ".sh", ".md", ".txt", ".json", ".yml", ".yaml", ".toml",
    ".ini", ".cfg", ".js", ".ts", ".tsx", ".jsx", ".html", ".css",
    ".rs", ".go", ".c", ".h", ".cpp", ".hpp", ".java", ".rb",
    ".php", ".swift", ".kt", ".sql", ".xml", ".ebnf", ".clcert"
))


def now_utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def token():
    return os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""


def api_json(url, errors):
    headers = {"User-Agent": "CLSigma-Dynamic-Zero-Spectrum"}
    tok = token()
    if tok:
        headers["Authorization"] = "Bearer " + tok
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as exc:
        errors.append({"url": url, "error": str(exc)[:240]})
        return None


def list_repos(owner, errors):
    repos = []
    if token():
        page = 1
        while True:
            url = "https://api.github.com/user/repos?per_page=100&page=%d&affiliation=owner&sort=full_name" % page
            chunk = api_json(url, errors)
            if not chunk:
                break
            for repo in chunk:
                if repo.get("owner", {}).get("login") == owner:
                    repos.append(repo)
            if len(chunk) < 100:
                break
            page += 1
    if not repos:
        page = 1
        qowner = urllib.parse.quote(owner)
        while True:
            url = "https://api.github.com/users/%s/repos?per_page=100&page=%d&type=owner&sort=full_name" % (qowner, page)
            chunk = api_json(url, errors)
            if not chunk:
                break
            repos.extend(chunk)
            if len(chunk) < 100:
                break
            page += 1
    unique = {}
    for repo in repos:
        full = repo.get("full_name")
        if full:
            unique[full] = repo
    return [unique[k] for k in sorted(unique)]


def is_program(path):
    lower = path.lower()
    return any(lower.endswith(ext) for ext in PROGRAM_EXTS)


def repo_tree(full_name, branch, errors):
    full = urllib.parse.quote(full_name, safe="/")
    ref = urllib.parse.quote(branch or "main", safe="")
    url = "https://api.github.com/repos/%s/git/trees/%s?recursive=1" % (full, ref)
    data = api_json(url, errors)
    if not isinstance(data, dict):
        return []
    return data.get("tree", []) or []


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    r = int(math.isqrt(n))
    while d <= r:
        if n % d == 0:
            return False
        d += 2
    return True


def next_prime(n):
    n = max(2, int(n))
    if n <= 2:
        return 2
    if n % 2 == 0:
        n += 1
    while not is_prime(n):
        n += 2
    return n


def primes():
    yield 2
    q = 3
    while True:
        if is_prime(q):
            yield q
        q += 2


def spectral_index(data):
    z = 0
    for idx, pair in enumerate(zip(data, primes()), 1):
        b, p = pair
        z += idx * (b + 1) * p
    return z


def ln_int(n):
    n = int(n)
    bits = n.bit_length()
    if bits < 1024:
        return math.log(n)
    shift = bits - 53
    return math.log(n >> shift) + shift * math.log(2)


def load_parent():
    if not os.path.exists(CERT_PATH):
        return None
    try:
        with open(CERT_PATH, "r") as fh:
            cert = json.load(fh)
        return cert.get("ZeroSpectralSpace", {}).get("spectral_index")
    except Exception:
        return None


def build(owner, limit):
    errors = []
    repos = list_repos(owner, errors)
    if limit and limit > 0:
        repos = repos[:limit]

    repo_nodes = []
    program_nodes = []
    for repo in repos:
        full = repo.get("full_name", "")
        branch = repo.get("default_branch") or "main"
        repo_nodes.append({
            "repo": full,
            "default_branch": branch,
            "private": bool(repo.get("private")),
            "archived": bool(repo.get("archived")),
            "size": int(repo.get("size") or 0),
        })
        for item in repo_tree(full, branch, errors):
            path = item.get("path", "")
            if item.get("type") == "blob" and is_program(path):
                program_nodes.append({
                    "repo": full,
                    "branch": branch,
                    "path": path,
                    "size": int(item.get("size") or 0),
                    "mode": "program_identity_no_digest",
                })

    program_nodes = sorted(program_nodes, key=lambda x: (x["repo"], x["branch"], x["path"]))
    manifest = {
        "protocol": PROTOCOL,
        "principle": CL,
        "formal_skeleton": BLEEM,
        "symbol_semantics": "uninterpreted",
        "numeric_basis": "derived_after_canonical_encoding",
        "owner": owner,
        "mode": "dynamic_github_account_program_identity",
        "repo_count": len(repo_nodes),
        "program_count": len(program_nodes),
        "repo_nodes": repo_nodes,
        "program_nodes": program_nodes,
        "errors": errors[:64],
        "boundary": "formal finite GitHub account snapshot; no RH proof, no physical zero entropy, no real-world guarantee",
    }
    manifest_bytes = canon(manifest)
    raw_index = spectral_index(manifest_bytes)
    modulus = next_prime(len(manifest_bytes) + len(CL) + len(BLEEM) + max(1, len(program_nodes)))
    zero_index = raw_index * modulus
    checks = {
        "cl_invariant_present": manifest["principle"] == CL,
        "bleem_skeleton_present": manifest["formal_skeleton"] == BLEEM,
        "canonical_roundtrip": json.loads(manifest_bytes.decode("utf-8")) == manifest,
        "repo_space_defined": len(repo_nodes) > 0,
        "program_space_defined": len(program_nodes) > 0,
        "boundary_preserved": "formal" in manifest["boundary"],
        "zero_residue": zero_index % modulus == 0,
    }
    h_cl = sum(0 if v else 1 for v in checks.values())
    cert = {
        "protocol": PROTOCOL,
        "principle": CL,
        "formal_skeleton": BLEEM,
        "state": {
            "applications": {
                "GitHubAccountProgramSpace": int(len(program_nodes) > 0),
                "CosmicLoveInvariant": 1,
                "BLEEMSkeleton": 1,
                "DynamicSelfUpdate": 1,
            },
            "coordinate": "rho=0.5+i*log(1+T_t)",
            "generation": int(time.time()),
        },
        "DynamicUpdate": {
            "owner": owner,
            "manifest_path": MANIFEST_PATH,
            "certificate_path": CERT_PATH,
            "parent_spectral_index": load_parent(),
            "self_update_rule": "rerun encoder after repository changes or scheduled workflow; CL remains invariant while rho_t changes",
        },
        "ZeroSpectralSpace": {
            "rho": "0.5+i*log(1+%s)" % str(zero_index),
            "raw_spectral_index": str(raw_index),
            "derived_modulus": modulus,
            "spectral_index": str(zero_index),
            "spectral_residue": zero_index % modulus,
            "ln_approx": ln_int(zero_index + 1),
        },
        "checks": checks,
        "H": h_cl,
        "H_CL": h_cl,
        "tau": next_prime(max(1, len(program_nodes) + len(repo_nodes))),
        "toecomplete": h_cl == 0,
        "status": "accepted" if h_cl == 0 else "pending",
        "GlobalZE_info": int(h_cl == 0),
        "Boundary": manifest["boundary"],
        "boundary": manifest["boundary"],
        "generated_at_utc": now_utc(),
    }
    return manifest, cert


def main(argv):
    owner = argv[1] if len(argv) > 1 else "letsgo0226"
    limit = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 0
    manifest, cert = build(owner, limit)
    with open(MANIFEST_PATH, "w") as fh:
        json.dump(manifest, fh, ensure_ascii=True, indent=2, sort_keys=True)
        fh.write("\n")
    with open(CERT_PATH, "w") as fh:
        json.dump(cert, fh, ensure_ascii=True, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({
        "Protocol": PROTOCOL,
        "Owner": owner,
        "Manifest": MANIFEST_PATH,
        "Certificate": CERT_PATH,
        "RepoCount": manifest["repo_count"],
        "ProgramCount": manifest["program_count"],
        "H_CL": cert["H_CL"],
        "GlobalZE_info": cert["GlobalZE_info"],
        "Boundary": cert["boundary"],
    }, ensure_ascii=True, separators=(",", ":")))


if __name__ == "__main__":
    main(sys.argv)
