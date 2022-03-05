# Docker container with Pandoc, PdfTex, XeLaTeX and LuaTeX installed

[![Build Status][build-img]][build-status]
[![Docker Image][docker-pulls-img]][docker_repo]
[![License][license]][license_link]

A Docker container with [`Pandoc`](http://pandoc.org/) and [`LaTeX`](https://www.latex-project.org)
(plus some image processing tools) installed.

```
$ docker run --rm -v `pwd`:/data adstewart/pandoc
```

---

## Example
Generate HTML from Markdown
```
$ docker run --rm -v `pwd`:/data adstewart/pandoc -o example.html example.md
```
---
Generate PDF from Markdown
```
$ docker run --rm -v `pwd`:/data adstewart/pandoc -o example.html example.md
```

---

## Credits

Adapted from (inter alia) Jan Philip Bernius's `docker-pandoc`,
<https://github.com/jpbernius/docker-pandoc>.


[license]: https://img.shields.io/github/license/arranstewart/docker-pandoc.svg?maxAge=2592000
[license_link]: https://github.com/arranstewart/docker-pandoc/blob/master/LICENSE
[build-img]: https://github.com/arranstewart/docker-pandoc/actions/workflows/build.yml/badge.svg?branch=master
[build-status]: https://github.com/arranstewart/docker-pandoc/actions/workflows/build.yml
[docker_repo]: https://hub.docker.com/r/adstewart/pandoc/
[docker-pulls-img]: https://img.shields.io/docker/pulls/adstewart/pandoc

