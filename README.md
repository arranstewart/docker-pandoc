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


## Building multiplatform images locally

To support Apple Silicon (arm64) and other platforms, we use Docker's `buildx`
with QEMU for emulation. Instructions for setup on your development machine follow
(assumes Ubuntu >= 20.04 and Docker is already installed).

### 1. Install QEMU

```bash
sudo apt update
sudo apt install -y qemu-user-static
```

Provides the necessary emulators so you can build `arm64` images on an `amd64` machine.

### 2. Enable experimental Docker CLI features (if needed)

Ensure Docker CLI experimental features are enabled:

```bash
mkdir -p ~/.docker
echo '{ "experimental": "enabled" }' > ~/.docker/config.json
```

(Often unnecessary with recent Docker versions, but can help avoid warnings.)

### 3. Set up a named `buildx` builder

We recommend creating a named builder to avoid interfering with your default Docker setup.

```bash
docker buildx create --name multiarch-builder
```

To list available builders and see their status:

```bash
docker buildx ls
```

Once created, you can explicitly use this builder for multi-platform builds without setting it as the default:

```bash
docker buildx build --builder=multiarch-builder --platform=linux/amd64,linux/arm64 -t yourimage:tag .
```

Add `--push` if you're building for multiple platforms and want to push to a remote registry. Without `--push`, you can only export a single-platform image to the local Docker daemon using `--load`.

### 4. Optional: Bootstrapping the builder (usually automatic)

If the builder isn't already bootstrapped (you’ll see a warning when building), you can do:

```bash
docker buildx inspect multiarch-builder --bootstrap
```

### Using the builder

Once this setup is done, you can build multi-platform images like so:

```bash
docker buildx build \
  --builder=multiarch-builder \
  --platform=linux/amd64,linux/arm64 \
  -t yourdockerhubuser/yourimage:dev \
  .
```

Or push directly to your registry:

```bash
docker buildx build \
  --builder=multiarch-builder \
  --platform=linux/amd64,linux/arm64 \
  -t ghcr.io/yourorg/yourimage:dev \
  --push \
  .
```

With recent versions of Docker, you can test images by specifying a
platform to run on, e.g.

```
docker -D run --rm -it \
		--platform linux/arm64 adstewart/pandoc:0.7
```


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



