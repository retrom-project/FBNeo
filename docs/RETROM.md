# Retrom FBNeo Web port

`retrom-fork.json` owns the upstream baseline, maintenance branch, adapter ABI and
closed release asset set. The upstream checkout and RetroArch frontend are pinned;
`.github/retrom/prepare.py` verifies the frontend commit before compiling.

The DAT is exported by `retrom_export_arcade_dat` from the exact shipped Wasm.
Only optional ROM entries are omitted. The paired provenance binds the core archive,
DAT, Wasm, source baseline, exporter and build configuration digests. Never substitute
a date-matched external DAT or relax mandatory-member validation.

Build with Python 3, Git, Docker, a C compiler, Node.js, and 7-Zip installed.
Emscripten is selected by immutable image digest in the candidate build script.

```sh
python3 -m unittest discover -s .github/rpg-runtime -p 'test_*.py'
bash .github/rpg-runtime/build-candidate.sh .cache/candidate
```

The candidate output directory must be empty. Source fingerprints cover tracked and
untracked source, including initialized submodules, while ignoring generated caches.
A dirty candidate is for local PFB validation only. Release packaging requires a
clean candidate at the tag commit and validates every declared file and checksum.

CI builds the same candidate and uploads it for review. The release workflow only
publishes existing annotated tags reachable from the maintenance branch. Product
acceptance and explicit publication authorization remain required before tagging.
