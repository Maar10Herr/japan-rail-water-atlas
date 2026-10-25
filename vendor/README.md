# MapLibre GL JS

The atlas vendors the production ES module, worker and CSS from **MapLibre GL JS 6.15.0**. They are embedded by `tools/build.py`; the renderer has no local code changes.

MapLibre's BSD 3-Clause notice, including its incorporated Mapbox and other notices, is preserved in [`../LICENSES/MapLibre-BSD-3-Clause.txt`](../LICENSES/MapLibre-BSD-3-Clause.txt). The [runtime dependency notices](../LICENSES/Renderer-Dependencies.md) are also
preserved, including in the single-file HTML. Third-party renderer and
dependency files retain their upstream licenses. The atlas's GPL-3.0-only license applies to the original atlas code and documentation.

The [renderer source distribution](https://github.com/Maar10Herr/japan-rail-water-atlas/releases/download/v0.2.0/renderer-corresponding-source.zip) contains the preferred MapLibre TypeScript, GLSL and CSS source, build scripts and configuration, the exact lockfile, both original runtime source maps, recovered dependency sources, the 17 pinned runtime package archives and their license texts. Its indexes record source paths, package registry URLs, integrity hashes and the shipped module checksums.

Upstream source is fixed to commit [`638b3f9ecab4b743fd4d086d3bfd19bce7b7b032`](https://github.com/maplibre/maplibre-gl-js/tree/638b3f9ecab4b743fd4d086d3bfd19bce7b7b032). The [full upstream source archive](https://github.com/maplibre/maplibre-gl-js/archive/638b3f9ecab4b743fd4d086d3bfd19bce7b7b032.tar.gz) also includes the test and benchmark fixtures omitted from the compact distribution.

To build the renderer from the supplied `maplibre-gl-js/` directory, use the Node.js version in `.nvmrc` (26), then run:

```sh
npm ci
npm run build-dist
```

`npm ci` installs locked build tools and runs the upstream code generation step. `build-dist` builds the stylesheet, Unicode and shader data, and development and production bundles. The three files used here are `dist/maplibre-gl.mjs`, `dist/maplibre-gl-worker.mjs` and `dist/maplibre-gl.css`. Dependencies are fetched from the registry; the source archive is not an offline npm cache.

The source archive was assembled by reading upstream archives and source maps. It has not been used to perform an independent renderer rebuild. The atlas HTML build is separate and described in the project README.
