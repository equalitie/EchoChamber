#! /usr/bin/env sh

SOURCE_FILES="src/chamber.go \
    src/clients.go \
    src/messagetypes.go"

echo "Formatting go files."
for file in `ls src/*.go`; do
  go fmt $file;
done

echo ""
echo "Installing dependencies."
echo "github.com/gorilla/mux"
go get github.com/gorilla/mux

echo ""
cd src/
echo "Running tests."
go test
cd ../

echo ""
go build $SOURCE_FILES && echo "Compiled successfully."
