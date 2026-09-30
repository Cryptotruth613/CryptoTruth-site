# CryptoTruth-site

The CryptoTruth website. No trackers, no cookies, no analytics, no third-party scripts or fonts.

## How it's organized

- `content/` holds everything you write or make.
  - `content/posts/<post-name>/` is one folder per Morning Post:
    - `post.md`: a few header lines, a line with `---`, then the article.
    - `meme.mp4`: the meme video.
    - `poster.jpg`: a still frame shown before the video plays.
  - `content/pages/`: the Start Here and About This Site pages.
  - `content/assets/`: the site's styling and script.
- `docs/` is the finished website that GitHub Pages publishes. It is generated; don't edit it by hand.
- `build.py` turns `content/` into `docs/`.

## Adding a Morning Post

1. Make a new folder in `content/posts/`, named like `the-quiet-bank-fail`.
2. Put in `meme.mp4`, `poster.jpg`, and a `post.md` like this:

```
number: 2
title: The Title of the Post
date: 2026-10-01
take: The short take, the same text as the social media post.
---
The full article in Markdown. ## makes a heading, > makes a pull quote.
```

3. Run `python build.py`, then commit and push. The site updates in a minute or two.

The signoff (-CryptoTruth-, © All Rights Reserved, Table of Contents), the archive, the gallery, and the home page list are all added automatically.
