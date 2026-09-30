"""Build the CryptoTruth website.

Reads everything in content/ and writes the finished site to docs/,
which is the folder GitHub Pages publishes.

    python build.py

Each post is one folder in content/posts/<slug>/ holding:
    post.md     the header lines, a line with ---, then the article in Markdown
    meme.mp4    the meme video
    poster.jpg  a still frame shown before the video plays (optional)
"""
import datetime
import html
import math
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SRC = ROOT / "content"
OUT = ROOT / "docs"
SITE_URL = "https://cryptotruth.co"

NAV = [
    ("posts/", "Morning Posts"),
    ("gallery/", "Meme Gallery"),
    ("start/", "Start Here"),
    ("about/", "About This Site"),
]
CHANNELS = [
    ("X", "https://x.com/cryptotruth"),
    ("YouTube", "https://www.youtube.com/@CryptoTruth411"),
    ("Discord", None),  # None = shown as "soon"
    ("Patreon", None),
]
SIG = '- @CryptoTruth - <em>Seeking Clarity in a Chaotic World</em>'
e = html.escape


# ---------- reading posts ----------

def read_post(folder):
    raw = (folder / "post.md").read_text(encoding="utf-8")
    head, _, body = raw.partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    date = datetime.date.fromisoformat(meta["date"])
    words = len(re.findall(r"\w+", body))
    return {
        "slug": folder.name,
        "folder": folder,
        "number": int(meta.get("number", 0)),
        "title": meta["title"],
        "date": date,
        "take": meta.get("take", ""),
        "sample": meta.get("sample", "").lower() in ("yes", "true"),
        "html": markdown.markdown(body, extensions=["extra", "smarty"]),
        "minutes": max(1, math.ceil(words / 220)),
        "video": (folder / "meme.mp4").exists(),
        "poster": (folder / "poster.jpg").exists(),
    }


def nice_date(d):
    return f"{d:%b} {d.day}, {d.year}"


# ---------- page shell ----------

def shell(depth, title, body, current=None, description="", rain=False):
    up = "../" * depth
    cur = ' aria-current="page"'
    nav = "\n".join(
        f'      <a href="{up}{href}"{cur if href == current else ""}>{label}</a>'
        for href, label in NAV
    )
    page_title = "CryptoTruth" if title is None else f"{e(title)} | CryptoTruth"
    desc = e(description or "Sound money, first principles, and the signal behind the noise.")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{page_title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<header class="top">
  <div class="top-inner">
    <a class="mark" href="{up}" aria-label="CryptoTruth home">CRYPTO<span>TRUTH</span></a>
    <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button>
    <nav class="nav" id="main-nav" aria-label="Main">
{nav}
    </nav>
  </div>
</header>
{body}
<footer>
  <div class="foot">
    <span class="sign">-CryptoTruth-</span>
    <span>&copy; All Rights Reserved</span>
    <span class="clean">Nothing on this site tracks you</span>
  </div>
</footer>
<script src="{up}assets/site.js"></script>
</body>
</html>
"""


def post_rows(posts, up):
    rows = []
    for p in posts:
        rows.append(f"""    <article class="post-row">
      <div class="meta">No. {p['number']:03d} &middot; {nice_date(p['date'])}</div>
      <div>
        <h3><a href="{up}posts/{p['slug']}/">{e(p['title'])}</a></h3>
        <p>{e(p['take'])}</p>
      </div>
    </article>""")
    return "\n".join(rows)


# ---------- pages ----------

def home(posts):
    latest = posts[:5]
    body = f"""<section class="hero" aria-label="CryptoTruth">
  <canvas id="rain" aria-hidden="true"></canvas>
  <div class="hero-inner">
    <h1 class="frame">Signal Over Noise</h1>
    <div class="sig">{SIG}</div>
  </div>
</section>
<main class="page">
  <section class="lede-band">
    <p>Sound money first. Right now Bitcoin is the elephant in the room. CryptoTruth is written from first principles for people who want to understand why.</p>
    <div><a class="btn" href="start/">New? Start here</a></div>
  </section>
  <section>
    <h2 class="box-title">Latest Morning Posts</h2>
    <div class="posts">
{post_rows(latest, "")}
    </div>
    <div class="all"><a href="posts/">All Morning Posts &rarr;</a></div>
  </section>
  <section class="note">
    <div>
      <h2>No trackers. No cookies. No analytics.</h2>
      <p>This site runs on ordinary hosting for now, so it can get up and publishing. The next phase moves it onto decentralized infrastructure that no single company can throttle, redirect, or take down.</p>
    </div>
    <a class="btn" href="about/">Read the plan</a>
  </section>
</main>"""
    return shell(0, None, body)


def archive(posts):
    body = f"""<main class="page">
  <div class="page-head" style="padding:0">
    <h1>Morning Posts</h1>
    <p>Every piece, newest first. Each one starts as a meme and ends as the full argument.</p>
  </div>
  <div class="posts">
{post_rows(posts, "../")}
  </div>
</main>"""
    return shell(1, "Morning Posts", body, current="posts/")


def gallery(posts):
    tiles = []
    for p in posts:
        img = f'<img src="../posts/{p["slug"]}/poster.jpg" alt="" loading="lazy">' if p["poster"] else ""
        tiles.append(f"""    <a class="tile" href="../posts/{p['slug']}/">{img}<small>No. {p['number']:03d}</small><span>{e(p['title'])}</span></a>""")
    body = f"""<main class="page">
  <div class="page-head" style="padding:0">
    <h1>Meme Gallery</h1>
    <p>Every meme in one place. Tap one to watch it and read the full piece behind it.</p>
  </div>
  <div class="gallery">
{chr(10).join(tiles)}
  </div>
</main>"""
    return shell(1, "Meme Gallery", body, current="gallery/")


def fragment_page(name, title, current):
    frag = (SRC / "pages" / f"{name}.html").read_text(encoding="utf-8")
    return shell(1, title, f'<main class="page">\n{frag}\n</main>', current=current)


def post_page(p, prev_p, next_p):
    up = "../../"
    video = ""
    if p["video"]:
        poster = ' poster="poster.jpg"' if p["poster"] else ""
        video = f"""    <div class="video">
      <video src="meme.mp4"{poster} controls muted loop playsinline preload="metadata" aria-label="{e(p['title'])} meme"></video>
    </div>
    <div class="sound">Tap the video for sound</div>"""
    sample = '<div class="sample">Example text. The real article replaces this.</div>\n' if p["sample"] else ""
    chips = []
    for name, url in CHANNELS:
        if url:
            chips.append(f'<a class="chip" href="{url}" rel="noopener">{name}</a>')
        else:
            chips.append(f'<span class="chip soon">{name} <small>soon</small></span>')
    prev_link = (f'<a href="{up}posts/{prev_p["slug"]}/"><small>&larr; Previous</small>{e(prev_p["title"])}</a>'
                 if prev_p else f'<a href="{up}posts/"><small>All posts</small>Morning Posts archive</a>')
    next_link = (f'<a class="next" href="{up}posts/{next_p["slug"]}/"><small>Next &rarr;</small>{e(next_p["title"])}</a>'
                 if next_p else f'<a class="next" href="{up}gallery/"><small>Browse</small>Meme Gallery</a>')
    body = f"""<div class="narrow">
  <section class="meme">
    <div class="crumb">Morning Post No. {p['number']:03d}</div>
{video}
    <h1>{e(p['title'])}</h1>
    <div class="meta-line"><span>{nice_date(p['date'])}</span><span>{p['minutes']} min read</span></div>
  </section>
  <section class="take" aria-label="The short take">
    <div class="label">The short take</div>
    <p>{e(p['take'])}</p>
  </section>
  <article class="prose">
{sample}{p['html']}
    <div class="signoff">
      <div class="name">-CryptoTruth-</div>
      <div class="rights">&copy; All Rights Reserved</div>
      <a class="toc" href="{up}posts/">Table of Contents</a>
    </div>
  </article>
  <section class="channels" aria-label="Follow and share">
    <div class="label">Follow the signal</div>
    <div class="chips">{''.join(chips)}</div>
    <div class="chips"><button class="chip" id="copy-link" type="button" data-url="{SITE_URL}/posts/{p['slug']}/">Copy link to this post</button></div>
    <div class="copied" id="copied" aria-live="polite"></div>
  </section>
  <nav class="pager" aria-label="More Morning Posts">
    {prev_link}
    {next_link}
  </nav>
</div>"""
    return shell(2, p["title"], body, current=None, description=p["take"])


def not_found():
    body = """<main class="page" style="text-align:center">
  <section class="meme">
    <h1 class="frame">Signal Lost</h1>
    <p>That page isn't here. Try the <a href="/posts/">Morning Posts</a> or head <a href="/">home</a>.</p>
  </section>
</main>"""
    return shell(0, "Page not found", body)


# ---------- build ----------

def write(rel, text):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(SRC / "assets", OUT / "assets")
    (OUT / ".nojekyll").write_text("")

    posts = [read_post(f) for f in (SRC / "posts").iterdir() if (f / "post.md").exists()]
    posts.sort(key=lambda p: (p["date"], p["number"]), reverse=True)

    write("index.html", home(posts))
    write("posts/index.html", archive(posts))
    write("gallery/index.html", gallery(posts))
    write("start/index.html", fragment_page("start", "Start Here", "start/"))
    write("about/index.html", fragment_page("about", "About This Site", "about/"))
    write("404.html", not_found())

    for i, p in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        write(f"posts/{p['slug']}/index.html", post_page(p, older, newer))
        for f in ("meme.mp4", "poster.jpg"):
            if (p["folder"] / f).exists():
                shutil.copy2(p["folder"] / f, OUT / "posts" / p["slug"] / f)

    print(f"Built {len(posts)} post(s) into {OUT}")


if __name__ == "__main__":
    main()
