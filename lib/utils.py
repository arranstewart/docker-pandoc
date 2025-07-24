#!/usr/bin/env python3

"""
print docker metadata to stdout
"""

import os
import shlex
import subprocess
import sys

from datetime import datetime, timezone

# pylint: disable=subprocess-run-check

def verbose_run(*args, **kwargs):
  """
  run a command verbosely.

  says what's being run, output to stderr
  """

  cmd = args[0]

  print("running: ", shlex.join(cmd), file=sys.stderr)
  print("command array: ", repr(cmd), file=sys.stderr)

  sys.stderr.flush()
  sys.stdout.flush()
  return subprocess.run(*args, **kwargs)

def checked_run(*args, **kwargs):
  """
  verbose_run, but with noisy error reporting
  """

  our_kwargs = dict(
    capture_output=True,
    text=True,
    check=False,
  )

  # favour our_kwargs
  kwargs = kwargs | our_kwargs

  result = verbose_run(*args, **kwargs)

  if result.returncode != 0:
    print(result)
    print(f"Command {result.args} failed with exit code {result.returncode}")
    print("stderr:")
    print(result.stderr)
  assert result.returncode == 0, f"Command {result.args} failed with exit code {result.returncode}"

  return result

def load_metadata_env(filename="METADATA.env") -> dict[str,str]:
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

def generate_more_metadata() -> dict[str,str]:
  """
  extract more metadata from environment.

  `date`, and `git_commit`
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

def get_github_metadata() -> dict[str,str]:
  """
  return data about the repository, if we're running
  a github actions pipeline.

  if we aren't, returns an empty dict
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

def get_image_path(image_version=None) -> str:
  """
  get full image "path", e.g. adstewart/pandoc:0.8,
  suitable either for desktop, or for GitHub pipeline runner

  """

  metadata = load_metadata_env()

  if not image_version:
    image_version = metadata["IMAGE_VERSION"]
  image_name = metadata["IMAGE_NAME"]

  gh_metadata = get_github_metadata()

  if gh_metadata:
    image = 'ghcr.io/' + gh_metadata["repo"] + f'/{image_name}:{image_version}'
  else:
    image = metadata["IMAGE_NAMESPACE"] + f'/{image_name}:{image_version}'

  return image


