#!/usr/bin/env python3

"""
test docker image
"""

# pylint: disable=subprocess-run-check

import pathlib
import sys
import tempfile

from os.path import (
  abspath,
  join,
  dirname,
)

lib_dir = abspath(join(dirname(__file__), '../lib'))
sys.path.insert(0, lib_dir)

from utils import (
  get_image_path,
  verbose_run,
  checked_run,
)

#def checked_run(*args, **kwargs):


def test_uname_works_ok(platform: str, image_path: str):
  """
  check that `uname -a` seems to work okay
  in image
  """

  result = checked_run(
    ['docker', '-D', 'run', '--rm', f'--platform={platform}', image_path,
    'sh', '-c', 'uname -a'
    ],
    capture_output=True,
    text=True,
  )

  uname_output = result.stdout.strip()

  match platform:
    case 'linux/amd64':
      output_ok = "x86_64" in uname_output
    case 'linux/arm64':
      output_ok = "aarch64" in uname_output
    case _:
      mesg = f"Don't know how to verify platform {platform} uname output {repr(uname_output)}"
      raise ValueError(mesg)

  assert output_ok, \
         f"uname output unexpected for platform {platform}, was: {repr(uname_output)}"

  print(f"uname output ok for platform {platform}. was: {repr(uname_output)}")


def test_pandoc_version_ok(platform: str, image_path: str):
  """
  check that `pandoc --version` seems to work okay
  in image
  """

  result = checked_run(
    ['docker', '-D', 'run', '--rm', f'--platform={platform}', image_path,
    'pandoc', '--version'
    ],
    capture_output=True,
    text=True,
  )

  pandoc_version_output = result.stdout.strip()

  output_ok = pandoc_version_output.startswith("pandoc ")

  assert output_ok, \
         "pandoc version output unexpected for " + \
         f"platform {platform}, was: {repr(pandoc_version_output)}"

  print(f"pandoc version ok for platform {platform}. was: {repr(pandoc_version_output)}")

def test_pdflatex_version_ok(platform: str, image_path: str):
  """
  check that `pdflatex --version` seems to work okay
  in image
  """

  result = checked_run(
    ['docker', '-D', 'run', '--rm', f'--platform={platform}', image_path,
    'pdflatex', '--version'
    ],
    capture_output=True,
    text=True,
  )

  pdflatex_version_output = result.stdout.strip()

  output_ok = pdflatex_version_output.startswith("pdfTeX ")

  assert output_ok, \
         "pdflatex version output unexpected for " + \
         f"platform {platform}, was: {repr(pdflatex_version_output)}"

  print(f"pdflatex version ok for platform {platform}. was: {repr(pdflatex_version_output)}")

def test_pandoc_conversion_ok(platform: str, image_path: str):
  """
  check that conversion from markdown to PDF via latex seems to work okay
  in image.

  """

  #tmpdir = tempfile.mkdtemp(prefix="pandoc-image-test-")

  tmp_args = {
    "prefix": "pandoc-image-test-"
  }

  # See <https://github.com/abiosoft/colima/issues/515#issuecomment-1353220835>.
  # colima is more limited on the bind-mounts it can create, compared to vanilla docker:
  # "The folder you are mounting needs to either be within $HOME or within
  # /tmp/colima, those are the only two directories mounted into the VM."
  #
  # Attempting to mount any other directory fails, **silently** (which is unhelpful) -
  # the "mounted" directory is just empty when viewed from within a container.
  # Issue for tracking this bug at <https://github.com/abiosoft/colima/issues/530>.

  if sys.platform == "darwin":
    print("Running on macOS, using a tmpdir under /tmp/colima")
    tmp_args["dir"] = "/tmp/colima"


  with tempfile.TemporaryDirectory(**tmp_args) as tmpdir:
  #if True:

    tmp = pathlib.Path(tmpdir)
    print("using tmp dir", tmp, file=sys.stderr)

    md_path = tmp / "test.md"
    md_path.write_text(
      "The word zugzwang refers to a **position where any move worsens your situation**.\n"
    )

    sys.stdout.flush()
    sys.stderr.flush()

    # what's in /work?
    result = checked_run(
      [
        'docker', '-D', 'run', '--rm', f'--platform={platform}',
        '--mount', f"type=bind,source={str(tmp)},target=/work",
        "--workdir=/work",
        image_path
      ] + ["sh", "-c", "set -x; pwd; ls -al .; echo >&2; echo"],
      capture_output=True,
      text=True,
    )

    ls_output = result.stdout.strip()
    print("\n\nresult of ls:", ls_output)
    ls_err = result.stderr.strip()
    print("err of ls:", ls_output)

    pandoc_cmd = ["pandoc", "-t", "latex", "-o", "/work/result.pdf", "/work/test.md"]

    # generate PDF
    result = checked_run(
      [
        'docker', '-D', 'run', '--rm', f'--platform={platform}',
        '--mount', f"type=bind,source={str(tmp)},target=/work",
        "--workdir=/work",
        image_path
      ] + pandoc_cmd,
      capture_output=True,
      text=True,
    )

    # convert PDF back to text
    result = checked_run(
      [
        'docker', '-D', 'run', '--rm', f'--platform={platform}',
        '--mount', f"type=bind,source={str(tmp)},target=/work",
        "--workdir=/work",
        image_path
      ] + ["pdftotext", "/work/result.pdf"],
      capture_output=True,
      text=True,
    )

    # check text file contains expected word
    txt_path = tmp / "result.txt"
    txt_conts = txt_path.read_text().strip()

    txt_ok = "zugzwang" in txt_conts

    assert txt_ok, \
           "contents of PDF unexpected for " + \
           f"platform {platform}, was: {repr(txt_conts)}"

    print(f"contents of PDF ok for platform {platform}. was: {repr(txt_conts)}")


def main() -> None:
  "main"

  args = sys.argv[1:]

  if args:
    platform = args[0]
  else:
    platform = 'linux/amd64'

  image_path = get_image_path()

  tests = [
    test_uname_works_ok, test_pandoc_version_ok,
    test_pdflatex_version_ok, test_pandoc_conversion_ok,
  ]

  for test in tests:
    sys.stdout.flush()
    sys.stderr.flush()

    print("\n\n[-] Running test", test.__name__, "\n")
    test(platform, image_path)


if __name__ == "__main__":
  main()


