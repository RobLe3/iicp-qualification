"""Exact pinned helper fragments in synthetic wrappers, not SDK/HTTP qualification.

This is reviewed local source reuse, NOT an untrusted-code execution sandbox.
No original test/campaign argv or SDK module is imported. Constructors and call
sites are inspected separately and are NOT covered by these fragment observations.
"""
from pathlib import Path
import ast,hashlib,json,subprocess,textwrap,threading,types
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'reports/postcert/2026-11-06-rate-helper-witnesses'
FRAGMENTS_SHA='c57a0cf828a5498c470e3ddc4f5a5e9b5202950efd9b07ae05af61404b2463b0'
VECTORS_SHA='23ac2c47ae6bf4cde0c72d2fff82efbe837e274cb296953c806806c6371275af'
NODE='node'
RUSTC='rustc'
PHP='php'

def digest(raw):return hashlib.sha256(raw).hexdigest()
def checked(raw,expected):
 if digest(raw)!=expected:raise ValueError('DIGEST_MISMATCH')
 return raw

def load_fragments(root=D):
 p=root/'fragments.json'
 if p.is_symlink():raise ValueError('SOURCE_PATH_UNSAFE')
 document=json.loads(checked(p.read_bytes(),FRAGMENTS_SHA));result={}
 for row in document['fragments']:
  code=row['code'];checked(code.encode(),row['fragment_sha256']);result[row['id']]=code
 if set(result)!={'python-relay','typescript-relay','rust-relay','rust-registration','php-redirect-clamp'}:raise ValueError('FRAGMENT_SET')
 return result

def load_vectors():return json.loads(checked((D/'vectors.json').read_bytes(),VECTORS_SHA))
def python_relay(fragment,vectors):
 # Only the exact method body is executed, on a deliberately synthetic holder.
 fn=ast.parse(textwrap.dedent(fragment)).body[0]
 if not isinstance(fn,ast.FunctionDef) or fn.name!='allow_bind' or fn.decorator_list:raise ValueError('METHOD_CONTRACT')
 scope={'__builtins__':{'len':len,'str':str,'bool':bool,'float':float},'RELAY_BIND_RATE_WINDOW_S':60.0,'time':types.SimpleNamespace(monotonic=lambda:(_ for _ in ()).throw(RuntimeError('CLOCK_NOT_AUTHORIZED')))}
 exec(compile(ast.Module(body=[fn],type_ignores=[]),'<pinned-relay-method>','exec'),scope)
 out=[]
 for case in vectors:
  holder=types.SimpleNamespace(_bind_rate_limit=case['limit'],_bind_rate_buckets={},_lock=threading.Lock())
  out.append([scope['allow_bind'](holder,step['source'],rebind=step['rebind'],now=step['now_ms']/1000) for step in case['steps']])
 return out

def generate_programs(fragments,vectors):
 js='const RELAY_BIND_RATE_WINDOW_MS = 60000;\nclass Witness {\n _bindRateBuckets = new Map();\n _bindRateLimit: number;\n constructor(limit: number) {this._bindRateLimit=limit;}\n'+fragments['typescript-relay']+'\n}\n'
 js+='const rows = '+json.dumps(vectors['relay'])+';\nconsole.log(JSON.stringify(rows.map(c=>{const w=new Witness(c.limit);return c.steps.map(s=>w.allowBind(s.source,{rebind:s.rebind,now:s.now_ms}));})));\n'
 rust='use std::{collections::HashMap,sync::Mutex,time::{Instant,Duration}};\nconst RELAY_BIND_RATE_WINDOW:Duration=Duration::from_secs(60);\nstruct Witness {bind_rate_limit:u32,bind_rate_buckets:Mutex<HashMap<String,(Instant,u32)>>}\nimpl Witness {\n'+fragments['rust-relay']+'\n}\n'+fragments['rust-registration']+'\nfn main(){let origin=Instant::now();\n'
 for case in vectors['relay']:
  rust+='{let w=Witness{bind_rate_limit:'+str(case['limit'])+',bind_rate_buckets:Mutex::new(HashMap::new())}; let values=vec!['
  rust+=','.join('w.allow_bind('+json.dumps(s['source'])+','+str(s['rebind']).lower()+',origin+Duration::from_millis('+str(s['now_ms'])+'))' for s in case['steps'])+'];println!("{:?}",values);}\n'
 for c in vectors['registration_step']:
  prev='None' if c['prev'] is None else 'Some(('+','.join(map(str,c['prev']))+'))'
  rust+='let (a,b)=register_rate_step('+prev+','+str(c['now_ms'])+','+str(c['ttl_ms'])+');println!("[{},{}]",a,b);\n'
 rust+='}\n'
 # config() is synthetic; response(), Symfony and the real middleware never run.
 php='<?php\nfunction config($key,$default){global $value;return $value;}\nfunction witness(){\n'+fragments['php-redirect-clamp']+'\nreturn $retry;}\n$out=[];\n'
 for c in vectors['retry_after_clamp']:php+='$value='+json.dumps(c['input'])+'; $out[]=witness();\n'
 php+='echo json_encode($out),"\\n";\n'
 return {'typescript-witness.mts':js,'rust-witness.rs':rust,'php-witness.php':php}

def run_bounded(argv,outdir,label,timeout=30):
 # Fixed local commands; timeout is per direct process, file size is checked after exit.
 # No process-tree deadline, streaming hard quota or sandbox is claimed.
 with (outdir/(label+'.stdout')).open('xb') as out,(outdir/(label+'.stderr')).open('xb') as err:
  r=subprocess.run(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,timeout=timeout,cwd=outdir)
 (outdir/(label+'.exit')).write_text(str(r.returncode)+'\n')
 for suffix in ['stdout','stderr']:
  if (outdir/(label+'.'+suffix)).stat().st_size>4*1024*1024:raise ValueError('CAPTURE_BOUND_EXCEEDED')
 if r.returncode:raise ValueError('COMMAND_FAILED_'+label)
 return (outdir/(label+'.stdout')).read_text()

def verify_observations(actual,vectors):
 expected={'python-relay':[[s['expected'] for s in c['steps']] for c in vectors['relay']],'typescript-relay':[[s['expected'] for s in c['steps']] for c in vectors['relay']],'rust-relay':[[s['expected'] for s in c['steps']] for c in vectors['relay']],'rust-registration':[c['expected'] for c in vectors['registration_step']],'php-redirect-clamp':[c['expected'] for c in vectors['retry_after_clamp']]}
 # JSON canonical equality avoids Python's bool/int equality weakening the gate.
 if json.dumps(actual,sort_keys=True)!=json.dumps(expected,sort_keys=True):raise ValueError('OBSERVATION_MISMATCH')
 return expected

def execute(output):
 fragments=load_fragments();vectors=load_vectors();output.mkdir(mode=0o700,exist_ok=False)
 for name,source in generate_programs(fragments,vectors).items():(output/name).write_text(source)
 actual={'python-relay':python_relay(fragments['python-relay'],vectors['relay'])}
 actual['typescript-relay']=json.loads(run_bounded([NODE,'--experimental-strip-types',str(output/'typescript-witness.mts')],output,'typescript'))
 run_bounded([RUSTC,'--edition=2021',str(output/'rust-witness.rs'),'-o',str(output/'rust-witness')],output,'rust-compile',60)
 rows=[json.loads(line) for line in run_bounded([str(output/'rust-witness')],output,'rust-execute').splitlines()];n=len(vectors['relay']);actual['rust-relay']=rows[:n];actual['rust-registration']=rows[n:]
 actual['php-redirect-clamp']=json.loads(run_bounded([PHP,str(output/'php-witness.php')],output,'php'))
 verify_observations(actual,vectors)
 result={'schema':'iicp.rate-helper-fragment-observations.v1','state':'OFFLINE_SYNTHETIC_FRAGMENTS_NOT_COMPONENT_QUALIFICATION','actual':actual,'relay_sequences_per_implementation':len(vectors['relay']),'relay_implementations':3,'registration_steps':len(vectors['registration_step']),'clamp_values':len(vectors['retry_after_clamp']),'qualification_credit':0,'original_case_argv_executed':False,'network_or_endpoint_executed':False,'full_constructor_or_callsite_executed':False}
 (output/'observations.json').write_text(json.dumps(result,indent=2)+'\n');return result

if __name__=='__main__':
 import sys
 import argparse,os
 parser=argparse.ArgumentParser(description='Offline pinned helper witnesses; no SDK, endpoint or qualification execution')
 parser.add_argument('action',choices=['verify','run'])
 parser.add_argument('--output',type=Path)
 parser.add_argument('--node',default='node');parser.add_argument('--rustc',default='rustc');parser.add_argument('--php',default='php')
 args=parser.parse_args();load_fragments();load_vectors()
 if args.action=='verify':
  if args.output:parser.error('--output is only valid for run')
  print('PASS: pinned fragment/vector integrity; no helper execution')
 else:
  if not args.output:parser.error('run requires a new --output directory')
  NODE,RUSTC,PHP=args.node,args.rustc,args.php
  old_umask=os.umask(0o077)
  try:r=execute(args.output.resolve())
  finally:os.umask(old_umask)
  print('PASS:36 SDK helper sequences +8 registration steps +8 clamp values;zero qualification credit')
