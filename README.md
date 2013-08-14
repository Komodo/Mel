# Mel
This is an extension to provide Maya Embedded Language (MEL) scripting support
to Komodo.

## About

This extension provides features such as:
* syntax highlighting (coloring)
* codeintel completions for variables and built-in functions
* smart indenting

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
