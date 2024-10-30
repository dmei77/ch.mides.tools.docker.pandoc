docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) mides/pandoc:latest "document.md" -o "document.pdf" --from markdown --template=eisvogel --pdf-engine=tectonic
