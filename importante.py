import concurrent.futures
import subprocess
import sys
from pkgutil import walk_packages

import test_package

code = """
import {name}
"""


if __name__ == "__main__":
    packages = walk_packages(test_package.__path__, test_package.__name__ + ".")

    def try_import(name):
        completed_process = subprocess.run(
            [
                sys.executable,
                "-c",
                code.format(name=name),
            ],
            # capture_output=True,
            # text=True,
            timeout=30,
        )
        if completed_process.returncode == 0:
            print(name, "OK")
        else:
            print(name, "FAILED")
            print(completed_process.stderr)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(try_import, [package.name for package in packages])
