# Palila

**Palila is a minimal, hackable, dependency-free Python static site generator.** There are [hundreds of Jamstack static site generators](https://jamstack.org/generators/). Palila was created to facilitate automated deployment of small websites on [LAMP stack](https://en.wikipedia.org/wiki/LAMP_(software_bundle)) servers with PHP and Python.

**How it works:** Palila crawls a directory tree and whenever it finds `index.md` it generates `index.html` according to `template.html` containing [mustache](https://mustache.github.io) tags.

### Features

* **No dependencies** - Runs on servers without access to `pip`
* **Folder names are URLs** - `index.html` is generated in folders containing `index.md`
* **No routing** - No need to engage PHP or `.htaccess` to route requests
* **Simple development** - Just markdown and Python (no Apache, PhP, or Docker)
* **Automated deployment** - A GitHub action requests `deploy.php` to `git pull` and `python build.py` to rebuild the site server-side.
* **Easy customization** - Syntax highlighting, table of contents, anchor headings, embedded YouTube videos, etc...

### Quickstart

```bash
palila.py --root ./demo --template demo/style/template.html
```

### About the Name

[Pelican](https://getpelican.com) is a full-featured static site generator powered by Python. Compared to the pelican, [the palila](https://en.wikipedia.org/wiki/Palila) is quite small.