MiDES pandoc Dockerfile
===================================================================

This repository contains a customized docker image of the pandoc:extra image. 

Basic Usage
--------------------------------------------------------------------------------

1. Install [Docker](https://www.docker.com) if you don't have it already.

2. Open a shell and navigate to wherever the files are that you want to convert.

   ```sh
   cd path/to/source/dir
   ```

   You can always run `pwd` to check whether you're in the right place.

4. [Run docker](https://docs.docker.com/engine/reference/run/) by entering the
   below commands in your favorite shell.

   Let's say you have a `README.md` in your working directory that you'd like to
   convert to HTML.

   ```sh
   docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/latex:3.4 README.md
   ```

   The `--volume` flag maps some directory on *your machine* (lefthand side of
   the colons) to some directory *in the container* (righthand side), so that
   you have your source files available for pandoc to convert. `pwd` is quoted
   to protect against spaces in filenames.

   Ownership of the output file is determined by the user executing pandoc *in
   the container*. This will generally be a user different from the local user.
   It is hence a good idea to specify for docker the user and group IDs to use
   via the `--user` flag.

   `pandoc/latex:3.4` declares the image that you're going to run. It's always a
   good idea to hardcode the version, lest future releases break your code.

   It may look weird to you that you can just add `README.md` at the end of this
   line, but that's just because the `pandoc/latex:3.4` will simply prepend
   `pandoc` in front of anything you write after `pandoc/latex:3.4` (this is
   known as the `ENTRYPOINT` field of the Dockerfile). So what you're really
   running here is `pandoc README.md`, which is a valid pandoc command.

   If you don't have the current docker image on your computer yet, the
   downloading and unpacking is going to take a while. It'll be (much) faster
   the next time. You don't have to worry about where/how Docker keeps these
   images.
