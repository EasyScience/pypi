# PyPi Repo
Simple slimline repo acting as a PyPi server for the easyScience universe. 

See [https://easyscience.github.io/pypi/](https://easyscience.github.io/pypi/)

# Using with pip
Simply install with the modified call:
```
pip install -v GSASII --extra-index-url https://easyscience.github.io/pypi/
```

# Using pyproject.toml 
Add the following to your `pyproject.toml`:
```
[[tool.poetry.source]]
name = "easyScience"
url = "https://easyscience.github.io/pypi/"
secondary = true
```
Dependencies can then be added the usual way
