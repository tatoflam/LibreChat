#!/bin/bash
set -e

echo "Building meguru-gdrive-mcp module..."
cd meguru-gdrive-mcp
npm install
npm run build
cd ..

echo "Build completed successfully!"
