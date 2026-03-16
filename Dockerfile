# Base Image
FROM pandoc/extra:3.5.0-ubuntu

# Labels -> http://label-schema.org/
LABEL ch.mides.tools.docker.pandoc.name = "pandoc"
LABEL ch.mides.tools.docker.pandoc.description = "This Docker image includes all the tools needed to generate PDFs with Pandoc."
LABEL ch.mides.tools.docker.pandoc.vendor = "MiDES"
LABEL ch.mides.tools.docker.pandoc.version = "0.0.4"
LABEL ch.mides.tools.docker.pandoc.maintainer = "dominic.meier@mides.ch"

COPY assets/packages.txt /root/packages.txt

ARG UID=1000
ARG GID=1000

# Install additional packages
RUN tlmgr update --self
RUN sed -e 's/ *#.*$//' -e '/^ *$/d' /root/packages.txt | \
    xargs tlmgr install \
  && rm -f /root/packages.txt

# Reduce image size: skip man pages, locales and docs during apt-get install
COPY ./assets/01_nodoc /etc/dpkg/dpkg.cfg.d/01_nodoc

# Reduce image size: disable apt package cache
COPY ./assets/02_nocache /etc/apt/apt.conf.d/02_nocache

# Install Inkscape. Before, update all package repositories
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    fonts-noto-cjk \
    fonts-noto-core \
    fonts-noto-extra \
    fonts-freefont-ttf \
    poppler-utils \
    inkscape \
    graphviz \
    librsvg2-bin

# Install python/pip and git
ENV PYTHONUNBUFFERED=1
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    python3 \
    python3-pip \
    python-is-python3 \
    git

COPY ./assets/pip.conf /etc/pip.conf
RUN pip3 install --no-cache --upgrade setuptools

# Install kroki filter dependencies (pandocfilters)
RUN pip3 install --no-cache pandocfilters

# Install patched kroki filter (PNG for Mermaid to fix missing text in PDF)
COPY assets/pandoc_kroki_filter.py /usr/local/bin/pandoc-kroki
RUN chmod +x /usr/local/bin/pandoc-kroki

# Fix panflute SyntaxWarning with Python 3.12+ (invalid escape sequence in docstring)
COPY assets/fix-panflute.py /tmp/fix-panflute.py
RUN python3 /tmp/fix-panflute.py && rm /tmp/fix-panflute.py

