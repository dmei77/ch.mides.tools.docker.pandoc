docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) mides/pandoc:latest "document.md" -o "document.html" --from markdown --lua-filter=pagebreak.lua
