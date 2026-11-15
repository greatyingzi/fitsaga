#!/usr/bin/env python3
import pathlib
P = pathlib.Path("/Users/liheng/work/self/fitsaga/.github/workflows/daily.yml")
s = P.read_text(encoding="utf-8")
s = s.replace("branches: [main, test]", "branches: [master, test]")
s = s.replace("github.ref == 'refs/heads/main'", "github.ref == 'refs/heads/master'")
P.write_text(s, encoding="utf-8")
print("workflow: main->master")
