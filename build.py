#!/usr/bin/env python3

"""
Build Docker images from directories containing Dockerfiles.
"""

# We want to support older Python versions so we will use the old style
# 'List[xzy]' type hint instead of the new 'list[xzy]' syntax.
# ruff: disable[UP035]
# ruff: disable[UP006]

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

# Top directory containing image directories
TOP_IMAGE_DIR = Path(__file__).resolve().parent


def get_all_image_directories(top_dir: Path) -> List[Path]:
    """
    Get all possible image directories that can be used to build an image.

    :param top_dir: The top-level directory to search for image directories.
    :return: List of image directories
    """

    dirs = []

    for directory in sorted(top_dir.iterdir()):
        if directory.is_dir() and (directory / 'Dockerfile').is_file():
            dirs.append(directory)

    return dirs

def get_image_tag_for_image_dir(image_dir: Path) -> str:
    """
    Generate a Docker image tag based on the image directory name.

    :param image_dir: The image directory.
    :return: Docker image tag.
    """

    # Preprocess directory name
    dir_name = image_dir.name
    dir_name = dir_name.replace(' ', '_')

    return f'moleculetest-{dir_name}'

def build_image_from_dir(image_dir: Path, pull: bool = True) -> int:
    """
    Build a Docker image from the specified directory.

    :param image_dir: The directory containing the Dockerfile.
    :param pull: Whether to use the --pull flag when building the image.
    :return: Exit code of the build process (0 if successful).
    """

    # Put together tag for image based on the directory name
    tag = get_image_tag_for_image_dir(image_dir)

    print(f'Building {tag} ...')
    try:
        # Put together docker command string
        cmd = ['docker', 'build']
        if pull:
            cmd.append('--pull')
        cmd.append(str(image_dir))
        cmd.extend(['-t', tag])

        subprocess.run(
            cmd,
            check=True,
        )
    except FileNotFoundError:
        print(
            'Error: docker was not found. Install Docker and add it to PATH.',
            file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(
            f'Error: building {tag} failed (exit code {error.returncode}).',
            file=sys.stderr)
        return error.returncode
    print()
    print()
    print()

    # No error occurred
    return 0

def main() -> int:
    """Main function"""

    # Get a list of all directories that are possible to build images from
    all_image_dirs = get_all_image_directories(TOP_IMAGE_DIR)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Build docker images')
    parser.add_argument(
        'images',
        nargs='*',
        metavar='IMAGE',
        help='Image directories to build (default: build all images).',
    )
    args = parser.parse_args()

    # Abort if we did not find any image directories
    if not all_image_dirs:
        parser.error('No image directories containing a Dockerfile were found.')

    # Check if given image directories are valid
    all_image_dir_names = [d.name for d in all_image_dirs]
    for given_dir in [d.strip('/') for d in args.images]:
        if given_dir not in all_image_dir_names:
            parser.error(
                f'Unknown image "{given_dir}". '
                f'Choose from: {", ".join(all_image_dir_names)}')

    # Build images from selected image directories
    selected_image_directories = (
        [TOP_IMAGE_DIR / image for image in args.images]
        if args.images else all_image_dirs
    )
    for image_dir in selected_image_directories:
        result = build_image_from_dir(image_dir)
        if result != 0:
            return result

    return 0


if __name__ == "__main__":
    sys.exit(main())
