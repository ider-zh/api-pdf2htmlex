# pdf2html 调用

run.py  api 服务

pdf2htmlEX 替代原有的 bin 程序



./pdf2htmlEX --embed-outline 0 --embed-css 1 --embed-font 0 --embed-external-font 0 --embed-image 1 --embed-javascript 0 --external-hint-tool ttfautohint --no-drm 0 --dest-dir ./tmp


```
sage: pdf2htmlEX [options] <input.pdf> [<output.html>]
  -f,--first-page <int>         first page to convert (default: 1)
  -l,--last-page <int>          last page to convert (default: 2147483647)
  --zoom <fp>                   zoom ratio
  --fit-width <fp>              fit width to <fp> pixels
  --fit-height <fp>             fit height to <fp> pixels
  --use-cropbox <int>           use CropBox instead of MediaBox (default: 1)
  --hdpi <fp>                   horizontal resolution for graphics in DPI (default: 144)
  --vdpi <fp>                   vertical resolution for graphics in DPI (default: 144)
  --embed <string>              specify which elements should be embedded into output
  --embed-css <int>             embed CSS files into output (default: 1)
  --embed-font <int>            embed font files into output (default: 1)
  --embed-image <int>           embed image files into output (default: 1)
  --embed-javascript <int>      embed JavaScript files into output (default: 1)
  --embed-outline <int>         embed outlines into output (default: 1)
  --split-pages <int>           split pages into separate files (default: 0)
  --dest-dir <string>           specify destination directory (default: ".")
  --css-filename <string>       filename of the generated css file (default: "")
  --page-filename <string>      filename template for split pages  (default: "")
  --outline-filename <string>   filename of the generated outline file (default: "")
  --process-nontext <int>       render graphics in addition to text (default: 1)
  --process-outline <int>       show outline in HTML (default: 1)
  --process-annotation <int>    show annotation in HTML (default: 0)
--process-form <int>          include text fields and radio buttons (default: 0)
--printing <int>              enable printing support (default: 1)
--fallback <int>              output in fallback mode (default: 0)
--tmp-file-size-limit <int>   Maximum size (in KB) used by temporary files, -1 for no limit. (default: -1)
--embed-external-font <int>   embed local match for external fonts (default: 1)
--font-format <string>        suffix for embedded font files (ttf,otf,woff,svg) (default: "woff")
--decompose-ligature <int>    decompose ligatures, such as ﬁ -> fi (default: 0)
--auto-hint <int>             use fontforge autohint on fonts without hints (default: 0)
--external-hint-tool <string> external tool for hinting fonts (overrides --auto-hint) (default: "")
--stretch-narrow-glyph <int>  stretch narrow glyphs instead of padding them (default: 0)
--squeeze-wide-glyph <int>    shrink wide glyphs instead of truncating them (default: 1)
--override-fstype <int>       clear the fstype bits in TTF/OTF fonts (default: 0)
--process-type3 <int>         convert Type 3 fonts for web (experimental) (default: 0)
--heps <fp>                   horizontal threshold for merging text, in pixels (default: 1)
--veps <fp>                   vertical threshold for merging text, in pixels (default: 1)
--space-threshold <fp>        word break threshold (threshold * em) (default: 0.125)
--font-size-multiplier <fp>   a value greater than 1 increases the rendering accuracy (default: 4)
--space-as-offset <int>       treat space characters as offsets (default: 0)
--tounicode <int>             how to handle ToUnicode CMaps (0=auto, 1=force, -1=ignore) (default: 0)
--optimize-text <int>         try to reduce the number of HTML elements used for text (default: 0)
--correct-text-visibility <int> try to detect texts covered by other graphics and properly arrange them (default: 0)
--bg-format <string>          specify background image format (default: "png")
--svg-node-count-limit <int>  if node count in a svg background image exceeds this limit, fall back this page to bitmap background; negative value means no limit. (default: -1)
--svg-embed-bitmap <int>      1: embed bitmaps in svg background; 0: dump bitmaps to external files if possible. (default: 1)
-o,--owner-password <string>  owner password (for encrypted files)
-u,--user-password <string>   user password (for encrypted files)
--no-drm <int>                override document DRM settings (default: 0)
--clean-tmp <int>             remove temporary files after conversion (default: 1)
--tmp-dir <string>            specify the location of temporary directory. (default: "/tmp")
--data-dir <string>           specify data directory (default: "/usr/local/share/pdf2htmlEX")
--poppler-data-dir <string>   specify poppler data directory (default: "")
--debug <int>                 print debugging information (default: 0)
--proof <int>                 texts are drawn on both text layer and background for proof. (default: 0)
-v,--version                  print copyright and version info
-h,--help                     print usage information
```
