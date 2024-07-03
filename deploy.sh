#!/bin/bash

cd frontend || exit
echo "Build Fronted Project"
npm run build
echo "Transfer the fronted into backend"
rm -rf ../backend/static && cp -r dist ../backend/static
cd ..
echo "Done"
