#!/bin/bash

set -e

echo "=================Building the AST Extractor java binary================="
cd engine/ingestion/ast-extractor
mvn clean package
echo "======================Built Java binary successfully!===================="

echo "=====================Moving ASTExtractor.jar to ingestion directory===================="
cp target/*-jar-with-dependencies.jar ../ASTExtractor.jar
echo "======================Moved ASTExtractor.jar to ingestion directory===================="

cd ../../../

echo "========================Build complete! ASTExtractor.jar is ready for the Python pipeline.========================"