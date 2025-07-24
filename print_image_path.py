#!/usr/bin/env python3

"""
print image 'path' to stdout.

first arg (if supplied) is a 'version' tag used to override the one
obtained from METADATA.env.
"""

# pylint: disable=subprocess-run-check

import os
import subprocess
import sys

from datetime import datetime, timezone

from os.path import (
  abspath,
  join,
  dirname,
)

lib_dir = abspath(join(dirname(__file__), 'lib'))
sys.path.insert(0, lib_dir)

from utils import (
  get_image_path,
)

def main():
  "main"

  args = sys.argv[1:]

  if args:
    image_path = get_image_path(args[0])
  else:
    image_path = get_image_path()

  assert (image_path.startswith("adstewart/pandoc:") or
           image_path.startswith("ghcr.io/arranstewart/docker-pandoc/pandoc:")), \
          f"unexpected image path {image_path}"

  print(image_path)

if __name__ == "__main__":
  main()


