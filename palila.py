import pathlib
import datetime
import markdown
import time
import argparse


def recursivelyMakeIndexes(folder: pathlib.Path, templateFile: pathlib.Path):
    """
    Recursively search folders for index.md convert them to index.html using the template
    """
    indexMarkdownFile = folder.joinpath("index.md")
    indexFile = folder.joinpath("index.html")
    if (indexMarkdownFile.exists()):
        if (indexFile.exists()):
            print(f"deleting\t{indexFile.resolve()}")
            indexFile.unlink()
        print(f"generating\t{indexFile}")
        pg = PageGenerator(indexMarkdownFile, templateFile)
        pg.save()
    for subFolder in [x for x in folder.glob("**/*") if x.is_dir()]:
        recursivelyMakeIndexes(subFolder, templateFile)


class PageGenerator:

    def __init__(self, markdownFile: pathlib.Path, templateFile: pathlib.Path):
        self.folder = markdownFile.parent
        self.timeStart = time.time()

        # validate paths are legit
        if markdownFile.exists() == False:
            raise Exception("does not exist: " + markdownFile.resolve())
        if (markdownFile.name != "index.md"):
            raise Exception("markdown files must be named index.md")
        if templateFile.exists() == False:
            raise Exception("does not exist: " + markdownFile.resolve())

        # break markdown into lines and identify which are code
        markdownLines = markdownFile.read_text(encoding="utf-8").split("\n")
        linesWithoutCode = self.getMarkdownLinesWithoutCode(markdownLines)

        # make anchors clickable and remember TOC items
        tocItems = []
        for i in linesWithoutCode:
            line = markdownLines[i]
            if "# [" in line:
                continue
            if (line.startswith("#")):
                hashes, title = line.split(" ", 1)
                markdownLines[i] = f"{hashes} [{title}](#{self._getTagUrl(title)})"
                tocItems.append([len(hashes), title])

        # replace one-line links with special content
        for i in linesWithoutCode:
            line = markdownLines[i]
            isLinkLine = line.startswith("![](") and line.strip().endswith(")")
            if not isLinkLine:
                continue

            url = line[4:-1]
            extension = url.lower().split(".")[-1]

            if extension == "png" or extension == "jpg" or extension == "gif":
                markdownLines[i] = f"<a href='{url}'><img src='{url}'></a>"
                continue

            if "://youtu" in line.lower():
                url = "https://www.youtube.com/embed/" + pathlib.Path(url).name
                markdownLines[i] = "<div class='ratio ratio-16x9 my-5'>" + \
                    f"<object class='border border-dark shadow' data='{url}'></object></div>"
                continue

        # add TOC to page
        for i in linesWithoutCode:
            if markdownLines[i].startswith("![](TOC)"):
                tocMarkdown = ""
                for level, title in tocItems:
                    tocMarkdown += "  " * level + \
                        f"* [{title}](#{self._getTagUrl(title)})\n"
                markdownLines[i] = tocMarkdown

        # convert markdown to HTML
        # https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions
        htmlLines = markdown.markdown("\n".join(markdownLines),
                                      extensions=['fenced_code', 'tables', 'meta', 'md_in_html']).split("\n")

        # add anchors to headings
        for i in self.getHtmlLinesWithoutCode(htmlLines):
            line = htmlLines[i]
            if line.startswith("<h") and "href" in line:
                anchorName = line.split('"')[1][1:]
                htmlLines[i] = line.replace(">", f" id='{anchorName}'>", 1)

        # read template and perform replacements
        html = templateFile.read_text()
        defaultReplacements = {
            "{{HEAD_TITLE}}": markdownFile.parent.name,
            "{{BUILD_UTC_DATE}}": str(datetime.datetime.utcnow().strftime("%x")),
            "{{BUILD_UTC_TIME}}": str(datetime.datetime.utcnow().strftime("%X")),
            "{{BUILD_TIME_MS}}": f"{(time.time() - self.timeStart) * 1000:.1f}",
            "{{CONTENT}}": "\n".join(htmlLines),
        }
        for key, value in defaultReplacements.items():
            html = html.replace(key, value)

        self.html = html

    def save(self, filename="index.html", deleteExisting=True):
        """
        Save the generated HTML as a file
        """
        outputFile = self.folder.joinpath(filename)
        if deleteExisting and outputFile.exists():
            outputFile.unlink()
        outputFile.write_text(self.html, encoding="utf-8")

    def getMarkdownLinesWithoutCode(self, markdownLines: list[str]) -> list[bool]:
        linesWithoutCode = []
        insideCodeBlock = False
        for i, line in enumerate(markdownLines):
            if (line.startswith("```")):
                insideCodeBlock = ~insideCodeBlock
            if (insideCodeBlock):
                continue
            else:
                linesWithoutCode.append(i)
        return linesWithoutCode

    def getHtmlLinesWithoutCode(self, htmlLines: list[str]) -> list[bool]:
        linesWithoutCode = []
        insideCodeBlock = False
        for i, line in enumerate(htmlLines):
            if "<pre>" in line:
                insideCodeBlock = True
                continue
            if "</pre>" in line:
                insideCodeBlock = False
                continue
            if not insideCodeBlock:
                linesWithoutCode.append(i)
        return linesWithoutCode

    def _getTagUrl(self, s: str):
        """
        Convert a string into a url-safe anchor tag
        """

        # must be lowercase
        tag = s.lower()

        # non-alphanumeric letters are replaced by dashes
        letters = list(tag)
        for i, letter in enumerate(letters):
            if letter.isalpha() or letter.isnumeric():
                continue
            letters[i] = "-"
        tag = "".join(letters)

        # disallow multiple dashes
        while "--" in tag:
            tag = tag.replace("--", "-")

        # disallow starting or ending with a dash
        tag = tag.strip("-")

        return tag


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build a website with Palila')
    parser.add_argument('-r', metavar='FOLDER', type=pathlib.Path, required=True,
                        help='root website folder to recursively search for markdown files')
    parser.add_argument('-p', metavar='FILE', type=pathlib.Path, required=True,
                        help='path to page template')
    args = parser.parse_args()

    rootPath = pathlib.Path(args.r).resolve()
    if not rootPath.exists() or not rootPath.is_dir():
        raise Exception(f"folder does not exist: {rootPath}")
    print(f"root folder: {rootPath}")

    pageTemplate = pathlib.Path(args.p).resolve()
    if not pageTemplate.exists() or not pageTemplate.is_file():
        raise Exception(f"file does not exist: {pageTemplate}")
    print(f"page template: {pageTemplate}")

    recursivelyMakeIndexes(rootPath, pageTemplate)
