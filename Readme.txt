This is an extension to provide Maya Mel scripting language support to Komodo.
This extension provides features such as:
* syntax highlighting (coloring)
* codeintel completions for variables and built-in functions
* smart indenting

The "mel-mainlex.udl" luddite file is used to generate the "Mel.lexres" file
that will be used by Komodo once the extension is installed.

Komodo's koext sdk tool can be used to perform the udl->lexres conversion and
also wrap the extension into a distributable xpi file:
 $ koext build

