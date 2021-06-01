"""
This script walks the through the demo folder and deletes all index.html files
"""

import pathlib
PATH_REPO = pathlib.Path(__file__).parent
import sys
sys.path.insert(0, str(PATH_REPO.joinpath("src")))
import palila

if __name__ == "__main__":
    demoFolder = PATH_REPO.joinpath("demo")
    palila.recursivelyDeleteIndexes(demoFolder)
