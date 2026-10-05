"""Package the owned core and the requirements exported by that exact Wasm."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[2]
output=Path(sys.argv[1]).resolve()
if not output.is_dir() or any(output.iterdir()):raise RuntimeError('CANDIDATE_OUTPUT_INVALID')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
fork=json.loads((root/'retrom-fork.json').read_text())
core='fbneo'
build=root/'.cache/retroarch'
notices=(root/'src/license.txt').read_bytes()+b'\nRetroArch frontend:\n'+(build/'COPYING').read_bytes()
with tempfile.TemporaryDirectory(dir=root/'.cache',prefix='package-') as temp:
 stage=Path(temp)
 for name in ('fbneo_libretro.js','fbneo_libretro.wasm'):shutil.copyfile(build/name,stage/name)
 (stage/'build.json').write_text(json.dumps({'minimumEJSVersion':'4.2.3','version':'retrom-content-result-v1'})+'\n')
 shutil.copyfile(root/'config/core.json',stage/'core.json')
 (stage/'license.txt').write_bytes(notices)
 for p in stage.iterdir():p.chmod(0o644);os.utime(p,(0,0))
 subprocess.run(['7z','a','-mtm=off','-mta=off','-mtc=off','-bd','-bso0','-bsp0','-t7z',str(output/'fbneo-wasm.data'),*sorted(p.name for p in stage.iterdir())],cwd=stage,check=True)
(output/'LICENSE').write_bytes(notices)
timestamp=datetime.fromtimestamp(1779944524,timezone.utc).isoformat()
(output/'fbneo.json').write_text(json.dumps({'core':core,'buildStart':timestamp,'buildEnd':timestamp,'options':json.loads((root/'config/core.json').read_text())['options']})+'\n')
subprocess.run([os.environ.get('RETROM_NODE','node'),str(root/'.github/retrom/export-dat.cjs'),str(output/'fbneo-arcade.dat')],check=True)
pair={'schemaVersion':1,'kind':'CORE_DAT_PAIR','core':{'filename':'fbneo-wasm.data','sha256':sha(output/'fbneo-wasm.data')},'dat':{'filename':'fbneo-arcade.dat','sha256':sha(output/'fbneo-arcade.dat')},'sourceCommit':fork['upstreams'][0]['commit'],'generator':{'method':'SHIPPED_WASM','symbol':'retrom_export_arcade_dat','wasmSha256':sha(build/'fbneo_libretro.wasm'),'sha256':sha(root/'.github/retrom/export-dat.cjs')},'buildConfigSha256':sha(root/'.github/retrom/compile.sh')}
(output/'fbneo-content-pair.json').write_text(json.dumps(pair,indent=2,sort_keys=True)+'\n')
subprocess.run([sys.executable,str(root/'.github/rpg-runtime/candidate_descriptor.py'),'finalize',str(output),'--core-id',core],check=True)
