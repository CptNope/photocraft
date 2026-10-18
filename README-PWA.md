# PhotoCraft GitHub Pages PWA

This fork adds an installable PWA wrapper to the original [PhotoCraft](https://github.com/storytold/photocraft) Rust/WebAssembly browser editor. It **builds the fork's source** and serves it as a static website on GitHub Pages. It is not affiliated with the original developers.

## Deploy

1. Go to [Settings → Pages](https://github.com/CptNope/photocraft/settings/pages) and set **Source: GitHub Actions**.
2. If this fork prompts to enable workflows, enable them under **Actions**.
3. Open [Deploy PhotoCraft PWA to GitHub Pages](https://github.com/CptNope/photocraft/actions/workflows/deploy-pwa.yml) and run the workflow, if it did not start from the commit.
4. After its deploy step succeeds, open **https://cptnope.github.io/photocraft/**.

A build can consume substantial RAM and runner resources because PhotoCraft compiles Rust to WebAssembly and optimizes its release binary. The release is not verified until the GitHub Actions build and deployment pass.

## PWA experience

- Android: use Chrome or a compatible browser's **Install app** / **Add to Home Screen**.
- iPad: use Safari → Share → **Add to Home Screen**.
- Desktop: install using the browser's app icon/menu where supported.

The updated build packages upstream's compressed WebAssembly app parts and boot module. Offline reopening depends on the device's available storage; test first launch online.

The build step generates generic app icons (not ArtCraft trademarks), a manifest, a scoped service worker, license notices and an installable web shell. It precaches the compiled JS/WASM and basic assets to support offline reopening. Browser storage limits may prevent full precaching; please open the app online at least once before going offline.

## Limitations

- The standalone web editor uses browser file pickers and downloads. **Save or Export before closing**; this build does not add cloud autosave.
- The PWA wrapper does not add AI tools, MCP support, or new Apple Pencil/S Pen features.
- GitHub Pages cannot execute PHP, a Rust MCP server, or a private AI API backend.
- The source uses MIT OR Apache-2.0 licensing. Keep upstream `NOTICE`, `LICENSE-MIT`, `LICENSE-APACHE` and `ATTRIBUTION.md`. ArtCraft's trademarks remain separate.
- For troubleshooting WASM MIME types, browser rendering, and fonts, see [upstream web hosting guidance](https://github.com/storytold/photocraft/blob/main/packaging/web/README.md).
