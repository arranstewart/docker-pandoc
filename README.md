# Docker container with Pandoc, PdfTex, and image-conversion tools installed

[![Build Status][build-img]][build-status]
[![Docker Image][docker-pulls-img]][docker_repo]
[![License][license]][license_link]

A Docker image based on Ubuntu 20.04, with software installed including:

- [Pandoc](http://pandoc.org/)
- [LaTeX](https://www.latex-project.org)
- [xcftools](https://github.com/j-jorge/xcftools/)
- [Inkscape](https://inkscape.org)
- [Pweave](https://github.com/mpastell/Pweave)
- [ImageMagick](https://imagemagick.org/)
- [Librsvg](https://wiki.gnome.org/Projects/LibRsvg)
- [LibreOffice Writer](https://www.libreoffice.org/discover/writer/)
- [Poppler utils](https://poppler.freedesktop.org)

----

## Credits

Adapted from (inter alia) Jan Philip Bernius's `docker-pandoc`,
<https://github.com/jpbernius/docker-pandoc>.


[license]: https://img.shields.io/github/license/arranstewart/docker-pandoc.svg?maxAge=2592000
[license_link]: https://github.com/arranstewart/docker-pandoc/blob/master/LICENSE
[build-img]: https://github.com/arranstewart/docker-pandoc/actions/workflows/build.yml/badge.svg?branch=master
[build-status]: https://github.com/arranstewart/docker-pandoc/actions/workflows/build.yml
[docker_repo]: https://hub.docker.com/r/adstewart/pandoc/
[docker-pulls-img]: https://img.shields.io/docker/pulls/adstewart/pandoc

