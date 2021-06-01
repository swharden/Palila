# Palila

**Palila is a minimal, hackable, dependency-free Python static site generator.** There are [hundreds of Jamstack static site generators](https://jamstack.org/generators/). Palila was created to facilitate automated deployment of small websites on [LAMP stack](https://en.wikipedia.org/wiki/LAMP_(software_bundle)) servers with PHP and Python but limited access to tools like node, go, and pip. Unlike PHP-dependent flat-file options (like my [md2html-php](https://github.com/swharden/md2html-php)), websites can be tested without requiring a PHP server and Docker.

* **No dependencies** - Runs on servers without access to `pip`
* **Folder names are URLs** - `index.html` is generated in folders containing `index.md`
* **No routing** - No need to engage PHP or `.htaccess` to route requests
* **Simple development** - Just VS Code and Python (no Apache/PHP server with Docker)
* **Automated deployment** - A GitHub action requests `deploy.php` to `git pull; python palila.py`
* **Easy customization** - Syntax highlighting, table of contents, anchor headings, embedded YouTube videos, etc...

### Quickstart

```python
import palila    
templateFile = "./demo/template.html"
demoFolder = "./demo/"
palila.recursivelyMakeIndexes(demoFolder, templateFile)
```

### Templating

Palila uses [mustache](https://mustache.github.io) logic-less template tags

```html
<title>{{TITLE}}</title>
```

### Development Status

This library was created with the intent only for the author to use it, but it is open-sourced (under the permissive MIT license) in case anyone else finds it useful.

### About the Name

[Pelican](https://getpelican.com) is a full-featured static site generator powered by Python. Compared to the pelican, [the palila](https://en.wikipedia.org/wiki/Palila) is quite small.