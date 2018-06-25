# PyCoPGit

This folder houses a presentation which you can
[view online](http://tbnorth.github.io/PyCoPGit).

The content of the presentation is in
[PyCoPGit](./PyCoPGit.md)

## Python CoP presentation details

Here is a description on the minutiae involved in generating
this presentation - you almost certainly don't want to read
it.  This presentation uses [reveal.js](https://revealjs.com/),
which uses a specially formatted markdown file to describe slides.
Usually you just clone the whole reveal.js repository and modify
it to include your slides, but it's ~5 Mb which I didn't want to
add to the Python_CoP repository.  That, and hosting at an URL
like http://tbnorth.github.io/PyCoPGit requires putting the content
on the `gh-pages` branch, of which there's only one per repository,
and I don't want my presentation to be the content seen at
http://USEPA.github.io/Python_CoP.  For these reasons I'm including
only my modified content here, so if you want to view this presentation
as a presentation:

 - `git clone https://github.com/hakimel/reveal.js.git`
 - copy the content of this folder into the reveal.js folder
 - start an HTTP server in that folder:
   - Python 2: `python -m SimpleHTTPServer`
   - Python 3: `python -m http.server`
 - view presentation at http://127.0.0.1:8000

Should future changes to reveal.js be incompatible with the
files provided here, do
```bash
git clone https://github.com/hakimel/reveal.js.git
cd reveal.js
git reset --hard a82c4333ed8c
```
to get the version of reveal.js I used for this presentation.
