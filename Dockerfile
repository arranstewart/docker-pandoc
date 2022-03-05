FROM ubuntu:20.04@sha256:8ae9bafbb64f63a50caab98fd3a5e37b3eb837a3e0780b78e5218e63193961f9
MAINTAINER Arran Stewart <arran.stewart@uwa.edu.au>

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y -o Acquire::Retries=10 --no-install-recommends \
    ca-certificates   \
    curl              \
    locales           \
    wget && \
  echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
  locale-gen en_US.utf8 && \
  /usr/sbin/update-locale LANG=en_US.UTF-8 && \
  # Removing doc packages after installing to reduce size
  apt-get --purge remove -y .\*-doc$ && \
  # Remove more unnecessary stuff
  apt-get autoclean && \
  apt-get clean -y && \
  apt-get --purge -y autoremove && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive \
    apt-get install -y -o Acquire::Retries=10 --no-install-recommends \
      epix                          \
      epstool                       \
      fontconfig                    \
      fonts-texgyre                 \
      ghostscript                   \
      graphviz                      \
      groff                         \
      imagemagick                   \
      inkscape                      \
      latexmk                       \
      lmodern                       \
      m4                            \
      make                          \
      ps2eps                        \
      pstoedit                      \
      pstotext                      \
      psutils                       \
      python-pygments               \
      texlive-bibtex-extra          \
      texlive-fonts-extra           \
      texlive-fonts-recommended     \
      texlive-font-utils            \
      texlive-latex-base            \
      texlive-latex-extra           \
      texlive-latex-recommended     \
      texlive-luatex                \
      texlive-pictures              \
      texlive-pstricks              \
      texlive-publishers            \
      texlive-science               \
      texlive-xetex                 \
      transfig && \
  # Removing doc packages after installing to reduce size
  apt-get --purge remove -y .\*-doc$ && \
  # Remove more unnecessary stuff
  apt-get autoclean && \
  apt-get clean -y && \
  apt-get --purge -y autoremove && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ARG PANDOC_VERSION=2.17.1.1
ARG PANDOC_DEB=pandoc-${PANDOC_VERSION}-amd64.deb
ARG PANDOC_URL=https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-1-amd64.deb

RUN \
  cd /tmp && \
  wget --no-check-certificate ${PANDOC_URL} && \
  sudo apt install --no-install-recommends tmp/${PANDOC_DEB} && \
  rm * && \
  apt-get clean

