// Execute the shipped Wasm, before main(), to export its own ROM table.
const fs = require('node:fs');
const path = require('node:path');
const root=path.resolve(__dirname,'../..');
const factory=require(path.join(root,'.cache/retroarch/fbneo_libretro.js'));
(async()=>{
 const module=await factory({noInitialRun:true,wasmBinary:fs.readFileSync(path.join(root,'.cache/retroarch/fbneo_libretro.wasm'))});
 if(module._retrom_content_load_result()!==0)throw Error('CONTENT_RECEIPT_NOT_PENDING');
 if(module._retrom_export_arcade_dat()!==0)throw Error('ROM_TABLE_EXPORT_FAILED');
 const bytes=module.FS.readFile('/fbneo-arcade.dat');
 if(bytes.length<1000)throw Error('ROM_TABLE_EXPORT_EMPTY');
 fs.writeFileSync(process.argv[2],bytes);
})();
