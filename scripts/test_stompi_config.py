import importlib.util,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric import ec
spec=importlib.util.spec_from_file_location('config',Path(__file__).with_name('stompi-config.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def decode(value):
 number=0
 for c in value:number=number*58+mod.ALPHABET.index(c)
 raw=b'\0'*(len(value)-len(value.lstrip('1')))+number.to_bytes((number.bit_length()+7)//8,'big')
 assert raw[-4:]==mod.hashlib.sha256(mod.hashlib.sha256(raw[:-4]).digest()).digest()[:4]
 return raw[:-4]
class Tests(unittest.TestCase):
 def test_keys_match_codec_and_each_other(self):
  public,secret=mod.authority_keys();p=decode(public);s=decode(secret)
  self.assertEqual(p[:2],b'\x01\x00');self.assertEqual(len(p),34);self.assertEqual(len(s),32)
  key=ec.derive_private_key(int.from_bytes(s,'big'),ec.SECP256K1());self.assertEqual(p[2:],key.public_key().public_numbers().x.to_bytes(32,'big'))
 def test_raw_rpc_string_and_json(self):
  with patch.object(mod.subprocess,'check_output',return_value=mod.GENESIS+'\n'):self.assertEqual(mod.rpc(['cli'],'getblockhash','0'),mod.GENESIS)
  with patch.object(mod.subprocess,'check_output',return_value='{"isvalid":true}'):self.assertEqual(mod.rpc(['cli'],'validateaddress','x'),{'isvalid':True})
 def test_private_file_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'pool.toml';mod.write_config(p,'config');self.assertEqual(p.stat().st_mode&0o777,0o600)
   with self.assertRaises(FileExistsError):mod.write_config(p,'changed')
   self.assertEqual(p.read_text(),'config')
if __name__=='__main__':unittest.main()
