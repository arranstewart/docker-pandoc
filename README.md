# Docker container with Pandoc, PdfTex, XeLaTeX and LuaTeX installed

[![License][license]][license_link]

A Docker container with [`Pandoc`](http://pandoc.org/) and [`LaTeX`](https://www.latex-project.org) installed.

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
[docker_repo]: https://hub.docker.com/r/adstewart/pandoc/

