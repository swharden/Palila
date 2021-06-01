import pathlib
import datetime
import markdown


def makeIndex(folder: pathlib.Path, templateFile: pathlib.Path):
    """
    Given a folder with index.md and a template, convert the markdown to HTML, 
    place it in the template, and save the output as index.html in the same folder.
    Optionally provide a dictionary of search/replace strings.
    """
    markdownFile = folder.joinpath("index.md")
    if markdownFile.exists() == False:
        raise Exception("does not exist: " + markdownFile.resolve())
    if templateFile.exists() == False:
        raise Exception("does not exist: " + markdownFile.resolve())

    # read markdown
    markdownText = markdownFile.read_text()

    # https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions
    markdownHtml = markdown.markdown(markdownText,
                                     extensions=['fenced_code', 'tables', 'codehilite', 'meta', 'toc'])

    # read template and perform replacements
    templateHtml = templateFile.read_text()
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
