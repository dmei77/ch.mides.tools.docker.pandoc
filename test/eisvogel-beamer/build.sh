cp "document.pdf" "document.old.pdf" 
docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) mides/pandoc:latest "document.md" -o "document.pdf" --from markdown --to=beamer --variable=theme:metropolis --variable=themeoptions:numbering=none
