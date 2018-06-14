FROM debian:sid
MAINTAINER Arran Stewart <arran.stewart@uwa.edu.au>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
  apt-get install -y -o Acquire::Retries=10 --no-install-recommends \
    fontconfig \
    lmodern \
    locales \
    python-pygments \
    texlive-bibtex-extra \
    texlive-fonts-extra \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-luatex \
    texlive-science \
    texlive-xetex \
    wget && \
  # Removing doc packages after installing to reduce size 
  apt-get --purge remove -y .\*-doc$ && \
  # Remove more unnecessary stuff
  apt-get autoclean && \
  apt-get clean -y && \
  apt-get --purge -y autoremove && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN \
  wget --no-check-certificate https://github.com/jgm/pandoc/releases/download/2.2.1/pandoc-2.2.1-1-amd64.deb && \
    dpkg -i pandoc* && \
    rm pandoc* && \
    apt-get clean

# Set the locale
RUN dpkg-reconfigure locales
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN mkdir /data
WORKDIR /data

CMD ["pandoc", "--help"]

