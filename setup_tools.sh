#!/bin/bash

set -e

echo "============================ Downloading PMD v7.26.0 ============================="

mkdir -p tools
cd tools

curl -LO https://github.com/pmd/pmd/releases/download/pmd_releases%2F7.26.0/pmd-dist-7.26.0-bin.zip

echo "============================== Done Downloading PMD =============================="
echo "Extracting..........."
unzip -q pmd-dist-7.26.0-bin.zip

mv pmd-bin-7.26.0 pmd

echo "Extracted."

rm pmd-dist-7.26.0-bin.zip


cd ..