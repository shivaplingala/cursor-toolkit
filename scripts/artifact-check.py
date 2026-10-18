#!/usr/bin/env python3
import json, os, py_compile, sys

def main(paths):
    fails = []
    py_read = open
    checkers = {".py": py_check, ".json": json_check}
    for p in paths:
        try:
            with py_read(p, errors="strict") as f:
                data = f.read()
        except OSError as e:
            fails.append(". ".join([p, "unreadable:", e.__class__.__name__]))
            continue
        if not data.strip():
            fails.append(". ".join([p, "empty"]))
            continue
        c = checkers.get(os.path.splitext(p)[1].lower())
        if c:
            err = c(p)
            if err:
                fails.append(". ".join([p, "malformed:", err]))
    if fails:
        for f in fails:
            print("FAIL", f)
        return 1
    print("OK", len(paths), "artifact(s) reopenable")
    return 0

def py_check(p):
    try:
        py_compile.compile(p, doraise=True)
    except py_compile.PyCompileError as e:
        return str(e).splitlines()[-1][:140]
    return None

def json_check(p):
    try:
        json.loads(open(p).read())
    except (ValueError, OSError) as e:
        return e.__class__.__name__ + ": " + str(e).splitlines()[-1][:140]
    return None

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or [sys.stdin.readline().strip()] if not sys.stdin.isatty() else []))
