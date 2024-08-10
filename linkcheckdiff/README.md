FTC Docs Linkcheck Diff
=======================

Adds the ability to check if linkcheck errors are new to 
the current iteration.


Installation
------------

1. Pip install extension 
`pip install git+https://github.com/FIRST-Tech-Challenge/ftcdocs-helper@main#subdirectory=linkcheckdiff`

2. Add extension to conf.py

```
extensions = [
    [other extensions]

    "ftcdocs_linkcheckdiff"
]
```
Usage
------

1. Add output.json from previous run to the same directory you run your make command and name it `main-output.json`. If this is your first run you can simply skip this step
2. Run `make linkcheckdiff`
3. View the result in `build/linkcheckdiff/output.json`
