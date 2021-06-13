---
Title: Template Tags
Description: Define page information in the frontmatter
Date: 2021-06-08 11PM EST
tags: blazor, csharp
noAds: true
---

# Template Tags

## Frontmatter

Add a header like this to your markdown to customize what is displayed in the template

```txt
---
Title: Working with 16-bit Images in CSharp
Description: A summary of how I work with 16-bit TIF file data in C# (using ImageMagick and LibTiff)
noAds: true
---
```

* `{{HEAD_TITLE}}` - content of `<title>`
* `{{HEAD_DESCRIPTION}}` - content of `meta name='description'`
* `{{ADS_WRAP_START}}` - gets replaced with `<!--` if ads are disabled with `noAds: true`
* `{{ADS_WRAP_END}}` - gets replaced with `-->` if ads are disabled with `noAds: true`

## Dynamic Information

Dynamic content can be placed in the _template_ (but not _pages_). Example template tags include:

* `{{BUILD_UTC_DATE}}` - day the page was _built_ (UTC time)
* `{{BUILD_UTC_TIME}}` - time the page was _built_ (UTC time)
* `{{BUILD_TIME_MS}}` - how long the page took to build (milliseconds)