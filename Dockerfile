# Base Image
FROM pandoc/extra:3.5.0-ubuntu

# Labels -> http://label-schema.org/
LABEL ch.mides.tools.docker.pandoc.name = "pandoc"
LABEL ch.mides.tools.docker.pandoc.description = "This Docker image includes all the tools needed to generate PDFs with Pandoc."
LABEL ch.mides.tools.docker.pandoc.vendor = "MiDES"
LABEL ch.mides.tools.docker.pandoc.version = "0.0.3"
LABEL ch.mides.tools.docker.pandoc.maintainer = "dominic.meier@mides.ch"

COPY assets/packages.txt /root/packages.txt


ARG UID=1000
ARG GID=1000

# Install additional packages
RUN tlmgr update --self
RUN sed -e 's/ *#.*$//' -e '/^ *$/d' /root/packages.txt | \
    xargs tlmgr install \
  && rm -f /root/packages.txt

# Install Inkscape. Before, update all package repositories 
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    fonts-noto-cjk \
    fonts-freefont-ttf \
    poppler-utils \
    inkscape \
    graphviz

# Install python/pip and git
ENV PYTHONUNBUFFERED=1
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    python3 \
    python3-pip \
    python-is-python3 \
    git

COPY ./assets/pip.conf /etc/pip.conf
RUN pip3 install --no-cache --upgrade setuptools

# Install kroki filter
RUN pip3 install git+https://gitlab.com/myriacore/pandoc-kroki-filter.git

