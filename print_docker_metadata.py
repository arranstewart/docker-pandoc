#!/usr/bin/env python3

"""
print docker metadata to stdout
"""

import os
import subprocess
import sys

from datetime import datetime, timezone

# pylint: disable=subprocess-run-check

def verbose_run(*cmd, **kwargs):
  "run a command verbosely"

  print("running: ", *cmd, file=sys.stderr)
  sys.stderr.flush()
  sys.stdout.flush()
  return subprocess.run(*cmd, **kwargs)

def load_metadata_env(filename="METADATA.env"):
  """
  read in an env file.

  we expect it will probably have UPPERCASE_NAMES, we dupe
  them as lowercase as well because why not
  """

  metadata: dict[str,str] = {}
  with open(filename, encoding="utf8") as ifp:
    for line in ifp:
      line = line.strip()
      if not line or line.startswith('#'):
        continue
      if '=' not in line:
        raise ValueError(f"Malformed line: {line}")
      key, value = line.split('=', 1)

      key = key.strip()
      value = value.strip().strip('"').strip("'")

      metadata[key] = value
      metadata[key.lower()] = value
  return metadata


def generate_more_metadata():
  """
  extract more metadata from environment
  """

  metadata = {}
  metadata["date"] = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

  result = verbose_run(
    ["git", "rev-parse", "HEAD"],
    capture_output=True,
    text=True,
    check=True
  )
  metadata["git_commit"] = result.stdout.strip()

  return metadata

def get_github_metadata():
  """
  return data about the repository, if we're running
  a github actions pipeline
  """

  gh_metadata = {}

  if os.environ.get("GITHUB_ACTIONS") == "true":
    gh_metadata["is-github"] = "true"

    # we expect this to be 'https://github.com':
    gh_metadata["server-url"] = os.environ["GITHUB_SERVER_URL"]

    # we expect this to be something like 'arranstewart/docker-pandoc':
    gh_metadata["repo"] = os.environ["GITHUB_REPOSITORY"]

    # we expect this to be ghcr.io or similar
    gh_metadata["registry"] = os.environ["REGISTRY"]

  return gh_metadata

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
    assert exp_label in metadata, f"Expected to see label {exp_label} in metadata, but did not: {metadata}"

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


