API documentation was taken from a known working kubernetes service

`jq '.groups[].versions[].groupVersion' apis.json | sed 's/"//g' | while read line; do curl -skq --create-dirs -o $line.json https://localhost:6443/apis/$line; done`
