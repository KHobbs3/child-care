#!/usr/bin/env bash

for filename in ./data/*/*;
do
   file -I ${filename}
done

# charset = character set file encoding.
