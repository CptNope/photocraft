#!/usr/bin/env python3
"""Package PhotoCraft's Trunk WASM build as a GitHub Pages PWA.
Uses only Python standard library; works at any relative Pages path.
"""
from __future__ import annotations
import json, math, os, shutil, struct, sys, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def make_icon(path: Path, size: int):
    """Original generic image-editor icon; does not use ArtCraft marks."""
    pixels = bytearray()
    for y in range(size):
        pixels.append(0)
        for x in range(size):
            u=(x+.5)/size
            v=(y+.5)/size
            r,g,b=(21,25,37)
            if .07<u<.93 and .07<v<.93:
                r,g,b=(32,48,68)
            if .22<u<.78 and .20<v<.80:
                r,g,b=(234,241,247)
            if .25<u<.75 and .23<v<.77:
                r,g,b=(57,80,113)
            if (u-.37)**2+(v-.37)**2 < .065**2:
                r,g,b=(250,197,96)
            if .27<u<.73 and .40<v<.73 and v>(.90-1.0*u) and v>(.17+.72*u):
                r,g,b=(84,209,221)
            pixels.extend((r,g,b,255))
    def chunk(kind,payload):
        return struct.pack(">I",len(payload))+kind+payload+struct.pack(">I",zlib.crc32(kind+payload)&0xffffffff)
    path.write_bytes(b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",size,size,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(bytes(pixels),9))+chunk(b"IEND",b""))

def prepare(site: Path):
    index=site/"index.html"
    if not index.is_file():
        raise SystemExit(f"Missing compiled PhotoCraft HTML: {index}")
    icons=site/"icons"
    icons.mkdir(parents=True,exist_ok=True)
    for name,size in (("icon-192.png",192),("icon-512.png",512),("apple-touch-icon.png",180)):
        make_icon(icons/name,size)
    shutil.copy2(ROOT/"pwa"/"manifest.webmanifest",site/"manifest.webmanifest")
    shutil.copy2(ROOT/"pwa"/"install-ui.js",site/"install-ui.js")
    for name in ("LICENSE-MIT","LICENSE-APACHE","NOTICE","ATTRIBUTION.md"):
        source=ROOT/name
        if source.is_file():
            shutil.copy2(source,site/name)
    (site/".nojekyll").touch()

    html=index.read_text(encoding="utf-8")
    if 'rel="manifest"' not in html:
        if "</head>" not in html:
            raise SystemExit("Built index.html has no closing head")
        head='''<link rel="manifest" href="./manifest.webmanifest">
<meta name="theme-color" content="#151925">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="apple-touch-icon" href="./icons/apple-touch-icon.png">
'''
        html=html.replace("</head>",head+"</head>",1)
    if "navigator.serviceWorker.register('./sw.js')" not in html:
        if "</body>" not in html:
            raise SystemExit("Built index.html has no closing body")
        script='''<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () =>
    navigator.serviceWorker.register('./sw.js')
      .catch(error => console.warn("PhotoCraft PWA registration failed",error)));
}
</script>
'''
        html=html.replace("</body>",script+"</body>",1)
    html=html.replace("</body>", '<script src="./install-ui.js" defer></script>\n</body>', 1)
    index.write_text(html,encoding="utf-8")

    assets=["./"+p.name for p in site.iterdir()
            if p.is_file() and p.suffix.lower() in (".wasm",".js",".css")]
    if not any(name.endswith(".wasm") for name in assets):
        raise SystemExit("No compiled WebAssembly file found")
    core=["./","./index.html","./manifest.webmanifest","./install-ui.js","./icons/icon-192.png",
          "./icons/icon-512.png","./icons/apple-touch-icon.png"]
    template=(ROOT/"pwa"/"sw.js").read_text(encoding="utf-8")
    version=(os.getenv("GITHUB_SHA") or "local")[:12]
    compiled=(template.replace("__BUILD_VERSION__",version)
              .replace("__PRECACHE_ASSETS__",json.dumps(sorted(set(core+assets)))))
    (site/"sw.js").write_text(compiled,encoding="utf-8")
    print(f"Packaged PhotoCraft PWA: {len(assets)} compiled assets, {site}")

if __name__ == "__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python3 pwa/prepare_site.py dist/web")
    prepare(Path(sys.argv[1]).resolve())
