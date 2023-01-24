+++
title = "Creating my Blog with Zola"
date = 2023-01-24
description = ""
+++

## Overview

Updating a website manually is pain.  Static site generators solve this and also allow your website to be hosted for free on services like GitHub/GitLab pages, Vercel, or Netlify.

While the [source](https://github.com/vishusandy/vishusandy.github.io) for this blog is on GitHub the details behind it warrant some explanation.  Hopefully this will be useful to anyone looking to start a tech/dev blog.


## Zola

I chose [Zola](https://www.getzola.org/) as a static site generator because it comes with all of the features I could want: generating a table of contents, a search feature, syntax highlighting, RSS, and a live preview while you're working.  I have yet to use them all.

It took a little while for me to learn how to use Zola but after that I started to like it a lot.  I have some gripes about their documentation but overall the program itself is very nice.

Zola is pretty easy to install; their [Installation](https://www.getzola.org/documentation/getting-started/installation/) page has many options.  Unfortunately the package for Fedora is fairly old so I had to use their [pre-built binares](https://github.com/getzola/zola/releases), otherwise things wouldn't work correctly in the live preview.

A simple `zola init` gets you started with a blank template.  Then use `zola serve --open` to preview your work as you go.  Finally you can start adding content in the `/content` directory or adding themes.  See the [Content Overview](https://www.getzola.org/documentation/content/overview/) and [Themes](https://www.getzola.org/documentation/themes/installing-and-using-themes/) pages for more details.

## Custom Theme

I opted to bypass the easy route and instead choose to make a plain looking theme aimed at tech/dev blogs.  You can find  [the theme](https://github.com/vishusandy/vishus_zola) on my GitHub with screenshots and installation instructions.

Some of the things I wanted:
- dead simple aesthetic (focus on content not the theme)
- mobile friendly design
- loads quickly
- support for math in markdown (I prefer [KaTeX](https://katex.org/))
- table of contents

To me those are the base requirements for a tech blog theme so I also added:

- if the page has been modified from the original verison it should show a link to the changes (if using Git)
- [Font Awesome](https://fontawesome.com/) - to display links to my GitHub and Mastodon as icons
- a link to scroll to the top of the page
- header and footer with custom links that can be edited in the `config.toml` instead of having to edit the templates.

Fortunately I was able to make all of that happen.  I will spare the details of creating the theme, but I will say it took a lot of effort.  Just because the theme "looks simple" doesn't mean it is behind the scenes.  My goal was to make it as flexible as possible without sacrificing features.

I ended up using template macros to build the header and footer.  This allows both the section and article templates to reuse that code.

You can find the custom theme [here](https://github.com/vishusandy/vishus_zola) along with installation instructions.

## GitHub Pages

I didn't want to manually upload changes, so I created a GitHub workflow to take the content from my Git repo and build the site everytime I push a change.  You can find the file I use [here](https://github.com/vishusandy/vishusandy.github.io/blob/main/.github/workflows/main.yml).

To set this up I went to my repo settings in GitHub, then selected "Deploy from a branch", selected the 'gh-pages' branch (with '/root' as the base folder).
