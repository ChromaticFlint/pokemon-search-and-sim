#!/bin/bash
# Simple build script for deployment platforms

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the project
echo "Building project..."
npm run build

echo "Build completed successfully!"
echo "Output directory: dist/"
ls -la dist/
