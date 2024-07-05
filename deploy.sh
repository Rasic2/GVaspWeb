#!/bin/bash

comment_start=$(cat -n backend/app.py | grep serve_index -B1 | head -1 | awk '{print $1}')
comment_end=$(cat -n backend/app.py | grep serve_static -A1 | tail -1 | awk '{print $1}')
echo "Uncomment the app.py"
sed -i "${comment_start},${comment_end} s/^# //" "backend/app.py"

cd frontend || exit
echo "Build Fronted Project"
npm run build
echo "Transfer the fronted into backend"
rm -rf ../backend/static && cp -r dist ../backend/static
cd ..
echo "Done"
