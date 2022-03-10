FROM ubuntu:20.04@sha256:8ae9bafbb64f63a50caab98fd3a5e37b3eb837a3e0780b78e5218e63193961f9
MAINTAINER Arran Stewart <arran.stewart@uwa.edu.au>

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y -o Acquire::Retries=10 --no-install-recommends \
    ca-certificates   \
    curl              \
    locales           \
    sudo              \
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
      default-jre \
      epix                          \
      epstool                       \
      fontconfig                    \
      fonts-texgyre                 \
      ghostscript                   \
      git                           \
      graphviz                      \
      groff                         \
      imagemagick                   \
      inkscape                      \
      latexmk                       \
      librsvg2-bin                  \
      libreoffice-java-common       \
      libreoffice-writer            \
      lmodern                       \
      m4                            \
      make                          \
      poppler-utils                 \
      ps2eps                        \
      pstoedit                      \
      pstotext                      \
      psutils                       \
      python-pygments               \
      python3-pip                   \
      python3-docutils              \
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
      transfig                      \
      unzip                         \
      xcftools && \
  # Removing doc packages after installing to reduce size
  apt-get --purge remove -y .\*-doc$ && \
  # Remove more unnecessary stuff
  apt-get autoclean && \
  apt-get clean -y && \
  apt-get --purge -y autoremove && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ARG PANDOC_VERSION=2.17.1.1
ARG PANDOC_DEB=pandoc-${PANDOC_VERSION}-1-amd64.deb
ARG PANDOC_URL=https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/${PANDOC_DEB}

RUN \
  cd /tmp && \
  wget ${PANDOC_URL} && \
  apt install $PWD/${PANDOC_DEB} && \
  rm pan* && \
  apt-get clean && \
  apt-get autoclean && \
  apt-get clean -y && \
  apt-get --purge -y autoremove && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# allow imagemagick conversions
# (see https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion)
RUN \
  sed -i '/^  <policy domain="coder"/ s/none/read|write/;' /etc/ImageMagick-6/policy.xml

ARG USER_NAME=user
ARG USER_ID=1001
ARG USER_GID=1001

RUN \
  addgroup --gid ${USER_GID} ${USER_NAME} && \
  adduser --home /home/${USER_NAME} --disabled-password --shell /bin/bash --gid ${USER_GID} --uid ${USER_ID} --gecos '' ${USER_NAME} && \
  echo "%${USER_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER ${USER_NAME}

ENV HOME=/home/${USER_NAME}
ENV PATH=/home/${USER_NAME}/.local/bin:$PATH

COPY requirements.txt /tmp/

RUN \
  pip3 install --user --upgrade pip==22.0.3 && \
  pip3 install -r /tmp/requirements.txt     && \
  sudo rm -rf /tmp/requirements.txt

ARG NONFREE_FONTS_INSTALLER_URL=https://www.tug.org/fonts/getnonfreefonts/install-getnonfreefonts

RUN : "install LaTeX non free fronts" && \
  curl -L -o /tmp/install-getnonfreefonts "$NONFREE_FONTS_INSTALLER_URL" && \
  chmod a+rx /tmp/install-getnonfreefonts && \
  sudo /tmp/install-getnonfreefonts && \
  sudo getnonfreefonts --sys --all && \
  sudo rm -rf /tmp/*

ARG P2_URL=https://github.com/wrouesnel/p2cli/releases/download/r11/p2-linux-x86_64

RUN : "install p2" && \
  curl -L -o ~/.local/bin/p2 "$P2_URL" && \
  chmod a+rx ~/.local/bin/p2

