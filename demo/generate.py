
import sys
import pathlib
sourceFolder = pathlib.Path(__file__).parent.joinpath("../src").resolve()
sys.path.insert(0, str(sourceFolder))

if True:
    import palila

if __name__ == "__main__":
    folderPath = pathlib.Path(__file__).parent
    templateFile = pathlib.Path(__file__).parent.joinpath("template.html")
    palila.makeIndex(folderPath, templateFile)
