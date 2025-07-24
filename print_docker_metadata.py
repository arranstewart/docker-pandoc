#!/usr/bin/env python3

"""
print docker metadata to stdout
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
  generate_more_metadata,
  get_github_metadata,
  load_metadata_env,
  verbose_run,
)

def main():
  "main"

  metadata = load_metadata_env()
  print("metadata:", metadata, "\n\n", file=sys.stderr)

  expected_labels = [
    "IMAGE_NAME",
    "IMAGE_VERSION",
    "IMAGE_TITLE",
    "IMAGE_DESCRIPTION",
    "IMAGE_LICENSE",
    "IMAGE_URL",
  ]

  for exp_label in expected_labels:
    assert exp_label in metadata, \
           f"Expected to see label {exp_label} in metadata, but did not: {metadata}"

  more_metadata = generate_more_metadata()
  print("more metadata:", more_metadata, "\n\n", file=sys.stderr)
  for k in more_metadata:
    metadata[k] = more_metadata[k]

  gh_metadata = get_github_metadata()
  if gh_metadata:
    repo_url = gh_metadata["server-url"] + "/" + gh_metadata["repo"]
  else:
    result = verbose_run(
      ["git", "config", "--get", "remote.origin.url"],
      capture_output=True,
      text=True,
      check=True
    )
    repo_url = result.stdout.strip()

  final_metadata = {
    "org.opencontainers.image.title": metadata["IMAGE_TITLE"],
    "org.opencontainers.image.description": metadata["IMAGE_DESCRIPTION"],
    "org.opencontainers.image.version": metadata["IMAGE_VERSION"],
    "org.opencontainers.image.licenses": metadata["IMAGE_LICENSE"],
    "org.opencontainers.image.revision": metadata["git_commit"],
    "org.opencontainers.image.source": repo_url,
    "org.opencontainers.image.created": metadata["date"],
    "org.opencontainers.image.url": metadata["IMAGE_URL"],
  }

  if gh_metadata:
    gh_vars = [
      "GITHUB_ACTION",
      "GITHUB_ACTOR",
      "GITHUB_BASE_REF",
      "GITHUB_HEAD_REF",
      "GITHUB_JOB",
      "GITHUB_REF",
      "GITHUB_REF_NAME",
      "GITHUB_REPOSITORY_ID",
      "GITHUB_REPOSITORY_OWNER",
      "GITHUB_RUN_ID",
      "GITHUB_WORKFLOW_REF",
      "RUNNER_OS",
    ]
    for var in gh_vars:
      val = os.environ.get(var)
      if val:
        final_metadata[var] = val

  for k in final_metadata:
    v = final_metadata[k]
    print(f"{k}={v}")


if __name__ == "__main__":
  main()


