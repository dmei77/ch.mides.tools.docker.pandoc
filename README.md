MiDES pandoc docker
===================================================================

This repository contains a customized docker image of the pandoc:extra image. 


Build
--------------------------------------------------------------------------------

1. Check sourcecode from github

2. Open a shell and navigate to the rootfolder of project

   ```sh
   cd ch.mides.tools.docker.pandoc
   ```

3. Run `build.sh`

   ```sh
   ./build.sh
   ```



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
   docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` mides/pandoc:latest README.md
   ```

   The `--volume` flag maps some directory on *your machine* (lefthand side of
   the colons) to some directory *in the container* (righthand side), so that
   you have your source files available for pandoc to convert. `pwd` is quoted
   to protect against spaces in filenames.

   Ownership of the output file is determined by the user executing pandoc *in
   the container*. This will generally be a user different from the local user.
   It is hence a good idea to specify for docker the user and group IDs to use
   via the `--user` flag.

   `mides/pandoc:latest` declares the image that you're going to run. 

   It may look weird to you that you can just add `README.md` at the end of this
   line, but that's just because the `mides/pandoc:latest` will simply prepend
   `pandoc` in front of anything you write after `mides/pandoc:latest`

