"""
Security utilities for blackhole-spin-pi project.

Implements basic security checks (P1-2 from joint audit).
"""

import re
import sys
import os


# Dangerous patterns to block
BLOCK_PATTERNS = [
    r"rm\s+-rf",           # rm -rf
    r"DROP\s+TABLE",        # SQL DROP TABLE
    r"TRUNCATE\s+TABLE",   # SQL TRUNCATE TABLE
    r"__import__",          # Python dynamic import
    r"os\.system",          # os.system calls
    r"subprocess\.Popen",   # subprocess calls
]

# Secret patterns to scan
SECRET_PATTERNS = [
    (r"sk-[a-zA-Z0-9]{48}", "OpenAI API Key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
    (r"xoxb-[a-zA-Z0-9-]{50,}", "Slack Bot Token"),
]


def check_dangerous_code(code_str):
    """
    Check if code contains dangerous patterns.
    
    Parameters:
    -----------
    code_str : str
        Code string to check
    
    Returns:
    --------
    dict : {"safe": bool, "blocked": list, "warnings": list}
    """
    result = {
        "safe": True,
        "blocked": [],
        "warnings": []
    }
    
    for pattern in BLOCK_PATTERNS:
        matches = re.findall(pattern, code_str, re.IGNORECASE)
        if matches:
            result["safe"] = False
            result["blocked"].append({
                "pattern": pattern,
                "matches": matches
            })
    
    return result


def scan_secrets(code_str):
    """
    Scan code for hardcoded secrets.
    
    Parameters:
    -----------
    code_str : str
        Code string to scan
    
    Returns:
    --------
    dict : {"clean": bool, "secrets": list}
    """
    result = {
        "clean": True,
        "secrets": []
    }
    
    for pattern, secret_name in SECRET_PATTERNS:
        matches = re.findall(pattern, code_str)
        if matches:
            result["clean"] = False
            result["secrets"].append({
                "type": secret_name,
                "count": len(matches)
            })
    
    return result


def security_check_file(filepath):
    """
    Security check for a file.
    
    Parameters:
    -----------
    filepath : str
        Path to file to check
    
    Returns:
    --------
    dict : Combined security check result
    """
    if not os.path.exists(filepath):
        return {"error": "File not found: {0}".format(filepath)}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    dangerous = check_dangerous_code(code)
    secrets = scan_secrets(code)
    
    return {
        "file": filepath,
        "dangerous": dangerous,
        "secrets": secrets,
        "overall_safe": dangerous["safe"] and secrets["clean"]
    }


def main():
    """CLI entry point for security checks."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Security check for blackhole-spin-pi code"
    )
    parser.add_argument(
        "files", nargs="+",
        help="Files to check"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output in JSON format"
    )
    
    args = parser.parse_args()
    
    results = []
    all_safe = True
    
    for filepath in args.files:
        result = security_check_file(filepath)
        results.append(result)
        if not result.get("overall_safe", False):
            all_safe = False
    
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            if "error" in result:
                print("[ERROR] {0}".format(result["error"]))
                continue
            
            status = "[SAFE]   " if result["overall_safe"] else "[UNSAFE]"
            print("\n{0}  {1}".format(status, result["file"]))
            
            if not result["dangerous"]["safe"]:
                print("  Blocked patterns:")
                for blocked in result["dangerous"]["blocked"]:
                    print("    - {0}: {1}".format(blocked["pattern"], blocked["matches"]))
            
            if not result["secrets"]["clean"]:
                print("  Secrets found:")
                for secret in result["secrets"]["secrets"]:
                    print("    - {0}: {1} occurrence(s)".format(secret["type"], secret["count"]))
    
    # Exit code
    sys.exit(0 if all_safe else 1)


if __name__ == "__main__":
    main()
