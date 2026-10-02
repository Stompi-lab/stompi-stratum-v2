#!/usr/bin/env python3
# Copyright (c) 2026 Stompi. Distributed under the MIT license (LICENSE-STOMPI).
import argparse,hashlib,json,os,re,subprocess
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ec

GENESIS='000000004ce46ead4546e107fc01668e9f3dafa15452a0766d9a03bc2167917b'
ALPHABET='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def base58check(payload):
 raw=payload+hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
 num=int.from_bytes(raw,'big');result=''
 while num:num,d=divmod(num,58);result=ALPHABET[d]+result
 return '1'*(len(raw)-len(raw.lstrip(b'\0')))+result

def authority_keys():
 key=ec.generate_private_key(ec.SECP256K1())
 secret=key.private_numbers().private_value.to_bytes(32,'big')
 public=key.public_key().public_numbers().x.to_bytes(32,'big')
 return base58check(b'\x01\x00'+public),base58check(secret)

def rpc(cli,*args):
 value=subprocess.check_output(cli+list(args),text=True,timeout=20).strip()
 try:return json.loads(value)
 except json.JSONDecodeError:return value

def render(public,secret,script,listen,tp):
 return f'''# Generated locally: contains a private pool key. Do not commit this file.
authority_public_key = {json.dumps(public)}
authority_secret_key = {json.dumps(secret)}
cert_validity_sec = 3600
listen_address = {json.dumps(listen)}
coinbase_reward_script = "raw({script})"
server_id = 1
pool_signature = "Stompi Stratum V2"
shares_per_minute = 6.0
share_batch_size = 10
monitoring_address = "127.0.0.1:19090"
monitoring_cache_refresh_secs = 15
[template_provider_type.Sv2Tp]
address = {json.dumps(tp)}
'''

def write_config(path,text):
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:
  with os.fdopen(fd,'w') as f:f.write(text);f.flush();os.fsync(f.fileno())
 except BaseException:
  Path(path).unlink(missing_ok=True);raise

def main():
 p=argparse.ArgumentParser(description='Create a Stompi SV2 pool configuration with fresh authority keys')
 p.add_argument('--address',required=True,help='Your own fallback STP payout address')
 p.add_argument('--cli',required=True);p.add_argument('--datadir',required=True);p.add_argument('--rpc-port',type=int,default=28432)
 p.add_argument('--listen',default='127.0.0.1:3334');p.add_argument('--template-provider',default='127.0.0.1:18442');p.add_argument('--output',default='stompi-pool.toml')
 a=p.parse_args()
 if Path(a.output).exists():raise SystemExit('Output exists; nothing overwritten.')
 if not 1<=a.rpc_port<=65535:raise SystemExit('Invalid RPC port')
 cli=[a.cli,'-datadir='+a.datadir,'-rpcport='+str(a.rpc_port)]
 if rpc(cli,'getblockhash','0')!=GENESIS:raise SystemExit('Wrong network: Stompi mainnet required.')
 info=rpc(cli,'validateaddress',a.address)
 if not isinstance(info,dict) or info.get('isvalid') is not True:raise SystemExit('Invalid Stompi payout address')
 script=info.get('scriptPubKey','')
 if not re.fullmatch(r'(?:[0-9a-f]{2})+',script) or len(script)>20000:raise SystemExit('Invalid payout script')
 public,secret=authority_keys();write_config(a.output,render(public,secret,script,a.listen,a.template_provider))
 print('Configuration saved:',a.output)
 print('Public pool key:',public)
 print('Private key stored only in the configuration. Keep it private.')
if __name__=='__main__':main()
