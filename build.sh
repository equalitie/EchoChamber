#! /usr/bin/env sh

SOURCE_FILES="src/chamber.go"

echo "Formatting go files."
for file in `ls src/*.go`; do
  go fmt $file;
done

echo ""
echo "Installing dependencies."

go build $SOURCE_FILES && echo "Compiled successfully."
