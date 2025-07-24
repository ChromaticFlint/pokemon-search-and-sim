#!/usr/bin/env node

// Custom build script for Vercel deployment
// This bypasses the permission issues with the vite binary

import { build } from 'vite';
import path from 'path';

async function buildApp() {
  try {
    console.log('Starting Vite build...');

    await build({
      root: process.cwd(),
      build: {
        outDir: 'dist',
        sourcemap: false,
        rollupOptions: {
          output: {
            manualChunks: undefined
          }
        }
      }
    });

    console.log('Build completed successfully!');
  } catch (error) {
    console.error('Build failed:', error);
    process.exit(1);
  }
}

buildApp();
