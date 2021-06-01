import pathlib
import markdown2
import datetime


def makeIndex(folder: pathlib.Path, templateFile: pathlib.Path):
    """
    Given a folder with index.md and a template, convert the markdown to HTML, 
    place it in the template, and save the output as index.html in the same folder.
    Optionally provide a dictionary of search/replace strings.
    """

    # read markdown
    markdownFile = folder.joinpath("index.md")
    if markdownFile.exists():
        markdownText = markdownFile.read_text()
        # https://github.com/trentm/python-markdown2/wiki/Extras
        markdownHtml = markdown2.markdown(markdownText,
                                          extras=["fenced-code-blocks", "tables"])
    else:
        raise Exception("does not exist: " + markdownFile.resolve())

    # read template
    if templateFile.exists():
        templateHtml = templateFile.read_text()
    else:
        raise Exception("does not exist: " + markdownFile.resolve())

    # perform replacements
    html = templateHtml.replace("{{CONTENT}}", markdownHtml)
    defaultReplacements = {
        "{{TITLE}}": folder.name,
        "{{DATE}}": str(datetime.datetime.now().strftime("%x")),
        "{{TIME}}": str(datetime.datetime.now().strftime("%X")),
    }
    for key, value in defaultReplacements.items():
        html = html.replace(key, value)

    # save output
    outputFile = folder.joinpath("index.html")
    outputFile.write_text(html)
    print(f"generated {outputFile.resolve()}")
