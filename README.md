# Mel
This is an extension to provide Maya Embedded Language (MEL) scripting support
to Komodo.

## About

This extension provides features such as:
* maps ".mel" files to the Mel language
* syntax highlighting (coloring)
* basic codeintel completions for variables, built-in functions and keywords
* smart brace indenting
* commenting/uncommenting support for "//"
* Code Intelligence API Catalog for Maya (thanks to JTilden)

## Installing

You can use Komodo's "Tools > Add-ons" dialog to install the add-on, since the
add-on is published on the Komodo community extension list:
http://community.activestate.com/xpi/maya-mel

## Building

Komodo's koext sdk tool can be used to perform the udl->lexres conversion and
also wrap the extension into a distributable xpi file:
 $ koext build

The "mel-mainlex.udl" luddite file is used to generate the "Mel.lexres" file
that will be used by Komodo once the extension is installed.
