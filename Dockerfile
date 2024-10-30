# Base Image
FROM pandoc/extra:3.5.0-ubuntu

# Labels -> http://label-schema.org/
LABEL ch.mides.tools.docker.pandoc.name = "pandoc"
LABEL ch.mides.tools.docker.pandoc.description = "Dieses Docker Image hat alle Tools für die Erzeugung von pdfs mit pandoc"
LABEL ch.mides.tools.docker.pandoc.vendor = "MiDES"
LABEL ch.mides.tools.docker.pandoc.version = "0.0.1"
LABEL ch.mides.tools.docker.pandoc.maintainer = "dominic.meier@mides.ch"


ARG UID=1000
ARG GID=1000

# Install Inkscape. Before, update all package repositories 
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    fonts-freefont-ttf \
    poppler-utils \
    inkscape \
    graphviz

# Install python/pip and git
#ENV PYTHONUNBUFFERED=1
#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
#    python3 \
#    python3-pip \
#    python-is-python3 \
#    git

