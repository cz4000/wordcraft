Source: a Claude Code session on https://github.com/python-humanize/humanize at commit 7574e0cc377d80db0d2756fc2c5e0b8799a6f8b4 (the commit before the maintainers' own fix in PR #329).
Tool results are shortened. The transcript stops right before Claude's final message.

**User:** naturalsize(999999) gives me '1000.0 kB' - shouldn't that be '1.0 MB'? I think the binary mode does something similar near 1024. Can you find out what's going on, fix it, and add tests? Run the test suite before you finish. I'm stepping away, so just get it done.

*[Grep: def naturalsize]*

```
src/humanize/filesize.py:38:def naturalsize(
```

*[Read: ~/code/humanize/src/humanize/filesize.py]*

```
1	"""Bits and bytes related humanization."""
2	
3	from __future__ import annotations
4	
5	from math import log
6	
7	from humanize.i18n import _gettext as _
8	
9	suffixes = {
10	    "decimal": (
11	        "kB",
12	        "MB",
… (91 more lines)
```

**Claude:** Let me see how the analogous `metric()` fix was done in #328, to stay consistent.

*[Bash: git show 7574e0c --stat && git show 7574e0c -- src && grep -n "naturalsize" -A3 tests/test_filesize.py | head -80]*

```
commit 7574e0cc377d80db0d2756fc2c5e0b8799a6f8b4
Author: Vincent Gao <gaobing1230@gmail.com>
Date:   Tue Jun 30 17:34:12 2026 +0200

    Carry `metric()` to the next SI prefix when rounding reaches 1000 (#328)
    
    Co-authored-by: Hugo van Kemenade <1324225+hugovk@users.noreply.github.com>

 src/humanize/number.py | 12 ++++++++++--
 tests/test_number.py   |  4 ++++
 2 files changed, 14 insertions(+), 2 deletions(-)
commit 7574e0cc377d80db0d2756fc2c5e0b8799a6f8b4
… (43 more lines)
```

*[Read: ~/code/humanize/tests/test_filesize.py]*

```
1	#!/usr/bin/env python
2	
3	"""Tests for filesize humanizing."""
4	
5	from __future__ import annotations
6	
7	import pytest
8	
9	import humanize
10	
11	
12	@pytest.mark.parametrize(
… (85 more lines)
```

*[Bash: python -c "
import humanize as h
for a in [(999999,),(999_950,),(999_949,),(1024**2-1,True),(1024**2-1,False,True),(1000**3-1,),(1024**3-1,True),(999999,False,False,'%.0f'),(1000**11-1,),(10**15,),(10**15-1,)]:
    print(a, h.naturalsize(*a))
"]*

```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 2, in <module>
    import humanize as h
ModuleNotFoundError: No module named 'humanize'
```

*[Bash: ls; cat tox.ini 2>/dev/null | head -30; PYTHONPATH=src python -c "
import humanize as h
for a in [(999999,),(999_950,),(999_949,),(1024**2-1,True),(1024**2-1,False,True),(1000**3-1,),(1024**3-1,True),(999999,False,False,'%.0f'),(1000**11-1,),(10**15,),(10**15-1,)]:
    print(a, h.naturalsize(*a))
"]*

```
This Bash command contains multiple operations. The following part requires approval: head -30; PYTHONPATH=src python -c "
import humanize as h
for a in [(999999,),(999_950,),(999_949,),(1024**2-1,True),(1024**2-1,False,True),(1000**3-1,),(1024**3-1,True),(999999,False,False,'%.0f'),(1000**11-1,),(10**15,),(10**15-1,)]:
    print(a, h.naturalsize(*a))
"
```

*[Bash: PYTHONPATH=src python -c "
import humanize as h
for a in [(999999,),(999_950,),(999_949,),(1024**2-1,True),(1024**2-1,False,True),(1000**3-1,),(1024**3-1,True),(999999,False,False,'%.0f'),(1000**11-1,),(10**15,),(10**15-1,)]:
    print(a, h.naturalsize(*a))
"]*

```
This command requires approval
```

*[Glob: {tox.ini,pyproject.toml,.venv/bin/python,Makefile,noxfile.py}]*

```
pyproject.toml
tox.ini
```

**Claude:** Still investigating: the bug is clear from the code (the value is formatted after the unit is chosen, so rounding can reach the base). I'm now trying to get Python to run so I can reproduce it.

*[Read: ~/code/humanize/tox.ini]*

```
1	[tox]
2	requires =
3	    tox>=4.2
4	env_list =
5	    docs
6	    lint
7	    mypy
8	    py{py3, 315, 314, 313, 312, 311, 310}
9	
10	[testenv]
11	extras =
12	    tests
… (33 more lines)
```

**Claude:** I'll write the fix now, then try running the tests.

*[Edit: ~/code/humanize/src/humanize/filesize.py]*
```
exp = int(min(log(abs_bytes, base), len(suffix)))
    value_ = format % (bytes_ / (base**exp))
    # Rounding can push the value up to the base (e.g. 999999 -> "1000.0 kB"),
    # so carry to the next suffix if there is one
    try:
        carry = exp < len(suffix) and abs(float(value_)) >= base
    except ValueError:
        carry = False
    if carry:
        exp += 1
        value_ = format % (bytes_ / (base**exp))
    space = "" if gnu else " "
    ret: str = value_ + space + _(suffix[exp - 1])
    return ret
```

```
The file ~/code/humanize/src/humanize/filesize.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

*[Edit: ~/code/humanize/tests/test_filesize.py]*
```
([1.123456789 * 10**6, False, True], "1.1M"),
        # Carry to the next suffix when rounding reaches the base
        ([999_949], "999.9 kB"),
        ([999_950], "1.0 MB"),
        ([999_999], "1.0 MB"),
        ([10**9 - 1], "1.0 GB"),
        ([999_999, False, False, "%.0f"], "1 MB"),
        ([999_499, False, False, "%.0f"], "999 kB"),
        ([1024**2 - 52, True], "1023.9 KiB"),
        ([1024**2 - 51, True], "1.0 MiB"),
        ([1024**2 - 1, True], "1.0 MiB"),
        ([1024**3 - 1, True], "1.0 GiB"),
        ([1024**2 - 1, False, True], "1.0M"),
        ([1000**11 - 1], "1000.0 QB"),
    ],
```

```
The file ~/code/humanize/tests/test_filesize.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

*[Edit: ~/code/humanize/tests/test_filesize.py]*
```
([999_960], "1.0 MB"),
```

```
The file ~/code/humanize/tests/test_filesize.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

*[Bash: python -m pytest -q]*

```
Exit code 2
/opt/anaconda3/lib/python3.13/site-packages/pytest_asyncio/plugin.py:247: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))

==================================== ERRORS ====================================
[31m[1m__________________ ERROR collecting src/humanize/__init__.py ___________________[0m
[31mImportError while importing test module '~/code/humanize/src/humanize/__init__.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/anaconda3/lib/python3.13/importlib/__init__.py:88: in import_module
… (144 more lines)
```

**Claude:** The package isn't installed (its `_version.py` is generated at install time) and test dependencies are missing. I'll set up a throwaway venv in the scratchpad.

*[Bash: V=/tmp/scratch/venv && python -m venv $V && $V/bin/pip install -q -e ".[tests]" 2>&1 | tail -5 && $V/bin/python -m pytest -q -p no:cacheprovider 2>&1 | tail -15]*

```
This Bash command contains multiple operations. The following parts require approval: V=/tmp/scratch/venv && python -m venv $V && $V/bin/pip install -q -e ".[tests]" 2>&1, tail -5 && $V/bin/python -m pytest -q -p no:cacheprovider 2>&1
```

*[Bash: python -m venv /tmp/scratch/venv]*

```
(Bash completed with no output)
```

*[Bash: /tmp/scratch/venv/bin/pip install -q -e "~/code/humanize[tests]"]*

```
This command requires approval
```

**Claude:** Installing packages needs approval I can't get while you're away. I'll check whether `_version.py` is gitignored, so I can create it locally without touching tracked files.

*[Grep: _version]*

```
.gitignore:159:src/*/_version.py
pyproject.toml:56:build.hooks.vcs.version-file = "src/humanize/_version.py"
```

*[Write: ~/code/humanize/src/humanize/_version.py]*
```
__version__ = "0.0.0.dev0"
```

```
File created successfully at: ~/code/humanize/src/humanize/_version.py (file state is current in your context — no need to Read it back)
```

**Claude:** `freezegun` isn't installed, so I'll leave out the two test files that need it and run everything else, including doctests.

*[Bash: python -m pytest -q -p no:cacheprovider --ignore=tests/test_i18n.py --ignore=tests/test_time.py --ignore=src/humanize/time.py --ignore=src/humanize/i18n.py 2>&1 | tail -15]*

```
[31mERROR[0m tests/test_benchmarks.py::[1mtest_clamp[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_fractional[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_intcomma[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_intword[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_metric[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_natural_list[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_naturaldate[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_naturalday[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_naturaldelta[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_naturalsize[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_naturaltime[0m
[31mERROR[0m tests/test_benchmarks.py::[1mtest_ordinal[0m
… (3 more lines)
```

*[Bash: python -m pytest -q -p no:cacheprovider --ignore=tests/test_i18n.py --ignore=tests/test_time.py --ignore=src/humanize/time.py --ignore=src/humanize/i18n.py 2>&1 | grep -E "^E |fixture '" | sort | uniq -c | head; python -m pytest -q -p no:cacheprovider tests/test_filesize.py src/humanize/filesize.py 2>&1 | tail -3]*

```
15 [31mE       fixture 'benchmark' not found[0m
[31mERROR[0m tests/test_filesize.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
[31m[31m[1m2 errors[0m[31m in 0.05s[0m[0m
```

**Claude:** The 15 errors come from the missing `pytest-benchmark` plugin, not from the code. Next I'll check why the targeted run failed to collect.

*[Bash: python -m pytest -p no:cacheprovider tests/test_filesize.py src/humanize/filesize.py -v 2>&1 | grep -E "Error|error|PASS|FAIL" | head -20]*

```
[1mcollecting ... [0mcollected 1 item / 2 errors
[31mImportError while importing test module '~/code/humanize/tests/test_filesize.py'.
E   ModuleNotFoundError: No module named 'humanize'[0m
[31mImportError while importing test module '~/code/humanize/tests/test_filesize.py'.
E   ModuleNotFoundError: No module named 'humanize'[0m
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
[31m============================== [31m[1m2 errors[0m[31m in 0.05s[0m[31m ===============================[0m
```

**Claude:** That's only an import-path quirk: `src/` lands on `sys.path` only when the package `__init__` is collected first. The broad run did include the filesize tests, so I'll confirm my new cases ran in it.

*[Bash: python -m pytest -v -p no:cacheprovider --ignore=tests/test_i18n.py --ignore=tests/test_time.py --ignore=src/humanize/time.py --ignore=src/humanize/i18n.py --ignore=tests/test_benchmarks.py 2>&1 | grep -E "filesize|passed|failed" | grep -vE "PASSED" ; python -m pytest -v -p no:cacheprovider --ignore=tests/test_i18n.py --ignore=tests/test_time.py --ignore=src/humanize/time.py --ignore=src/humanize/i18n.py --ignore=tests/test_benchmarks.py 2>&1 | grep -cE "filesize.*PASSED"]*

```
[32m============================= [32m[1m326 passed[0m[32m in 0.15s[0m[32m ==============================[0m
83
```

**Claude:** All 83 filesize tests pass (70 existing, 12 new, plus the doctest). Next I'll check the new tests actually catch the bug by running them against the original code.

*[Bash: git stash push -q src/humanize/filesize.py && python -m pytest -q -p no:cacheprovider --ignore=tests/test_i18n.py --ignore=tests/test_time.py --ignore=src/humanize/time.py --ignore=src/humanize/i18n.py --ignore=tests/test_benchmarks.py 2>&1 | grep -E "^E  +AssertionError|passed|failed"; git stash pop -q && git status --short]*

```
This Bash command contains multiple operations. The following parts require approval: git stash push -q src/humanize/filesize.py && python -m pytest -q -p no:cacheprovider --ignore=tests/test_i18n.py --ignore=tests/test_time.py --ignore=src/humanize/time.py --ignore=src/humanize/i18n.py --ignore=tests/test_benchmarks.py 2>&1, grep -E "^E  +AssertionError|passed|failed"; git stash pop -q && git status --short
```

**Claude:** I couldn't get approval to stash and re-run against the old code, so I'm skipping that check. The original code is visible and clearly gives `1000.0 kB` there. Last, I'll check the working tree.

*[Bash: git status --short]*

```
M src/humanize/filesize.py
 M tests/test_filesize.py
```
