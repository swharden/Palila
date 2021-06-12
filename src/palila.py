import pathlib
import datetime
import markdown
import time


def recursivelyDeleteIndexes(folder: pathlib.Path):
    """
    Recursively search for and delete index.html
    """
    indexFile = folder.joinpath("index.html")
    if (indexFile.exists()):
        print(f"deleting {indexFile.resolve()}")
        indexFile.unlink()
    for subFolder in [x for x in folder.glob("**/*") if x.is_dir()]:
        recursivelyDeleteIndexes(subFolder)


def recursivelyMakeIndexes(folder: pathlib.Path, templateFile: pathlib.Path):
    """
    Recursively search folders for index.md convert them to index.html using the template
    """
    makeIndex(folder.joinpath("index.md"), templateFile)
    for subFolder in [x for x in folder.glob("**/*") if x.is_dir()]:
        recursivelyMakeIndexes(subFolder, templateFile)


def safeUrl(s: str):
    # TODO: make better
    s = s.replace(" ", "-")
    s = s.lower()
    return s


def makeIndex(markdownFile: pathlib.Path, templateFile: pathlib.Path):
    """
    Convert the given index.md to index.html using the template
    """
    if markdownFile.exists() == False:
        raise Exception("does not exist: " + markdownFile.resolve())
    if (markdownFile.name != "index.md"):
        raise Exception("markdown files must be named index.md")
    if templateFile.exists() == False:
        raise Exception("does not exist: " + markdownFile.resolve())
    timeStart = time.time()

    # read markdown
    markdownLines = markdownFile.read_text().split("\n")

    # make anchors clickable and remember TOC items
    insideCodeBlock = False
    tocItems = []
    for i, line in enumerate(markdownLines):
        if (line.startswith("```")):
            insideCodeBlock = ~insideCodeBlock
        if (insideCodeBlock):
            continue
        if "# [" in line:
            continue
        if (line.startswith("#")):
            hashes, title = line.split(" ", 1)
            markdownLines[i] = f"{hashes} [{title}](#{safeUrl(title)})"
            tocItems.append([len(hashes), title])

    # add TOC to page
    insideCodeBlock = False
    for i, line in enumerate(markdownLines):
        if (line.startswith("```")):
            insideCodeBlock = ~insideCodeBlock
        if (insideCodeBlock):
            continue
        if line.startswith("![](TOC)"):
            tocMarkdown = ""
            for level, title in tocItems:
                tocMarkdown += "  " * level + \
                    f"* [{title}](#{safeUrl(title)})\n"
            markdownLines[i] = tocMarkdown

    # https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions
    markdownHtml = markdown.markdown("\n".join(markdownLines),
                                     extensions=['fenced_code', 'tables', 'meta', 'md_in_html'])

    # read template and perform replacements
    html = templateFile.read_text()
    defaultReplacements = {
        "{{HEAD_TITLE}}": markdownFile.parent.name,
        "{{BUILD_UTC_DATE}}": str(datetime.datetime.utcnow().strftime("%x")),
        "{{BUILD_UTC_TIME}}": str(datetime.datetime.utcnow().strftime("%X")),
        "{{BUILD_TIME_MS}}": f"{(time.time() - timeStart) * 1000:.1f}",
        "{{CONTENT}}": markdownHtml,
    }
    for key, value in defaultReplacements.items():
        html = html.replace(key, value)

    # save output
    outputFile = markdownFile.parent.joinpath("index.html")
    outputFile.write_text(html)
    print(f"generated {outputFile.resolve()}")
