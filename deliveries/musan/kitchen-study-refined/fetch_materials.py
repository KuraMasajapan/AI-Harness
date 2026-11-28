"""Download selected CC0 photographic PBR sets and a sunset panorama via the API."""
import concurrent.futures
import hashlib
import json
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
ASSETS=('fine_grained_wood','dark_wood','rough_linen','marble_01')
HEADERS={'User-Agent':'Nalu-Musan-Room-Prototype/1.0'}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=60).read()

def fetch(asset):
    directory=WORK/'sources'/asset
    directory.mkdir(parents=True,exist_ok=True)
    metadata=json.loads(get('https://api.polyhaven.com/files/'+asset))
    result={'asset':asset,'url':'https://polyhaven.com/a/'+asset,'license':'CC0-1.0','files':{}}
    for channel in ('Diffuse','nor_gl','Rough'):
        entry=metadata[channel]['1k']['jpg']
        path=directory/(channel+'.jpg')
        if not path.exists():path.write_bytes(get(entry['url']))
        data=path.read_bytes()
        if entry.get('md5'):assert hashlib.md5(data).hexdigest()==entry['md5']
        result['files'][channel]={'path':str(path.relative_to(ROOT)),
                                  'download_url':entry['url'],'sha256':hashlib.sha256(data).hexdigest()}
    return result

def fetch_sunset():
    asset='qwantani_sunset';directory=WORK/'sources'/asset
    directory.mkdir(parents=True,exist_ok=True)
    metadata=json.loads(get('https://api.polyhaven.com/files/'+asset))
    entry=metadata['hdri']['2k']['hdr'];path=directory/'sunset-2k.hdr'
    if not path.exists():path.write_bytes(get(entry['url']))
    data=path.read_bytes();assert hashlib.md5(data).hexdigest()==entry['md5']
    return {'asset':asset,'url':'https://polyhaven.com/a/'+asset,'license':'CC0-1.0',
            'files':{'HDR_2k':{'path':str(path.relative_to(ROOT)),'download_url':entry['url'],
                              'sha256':hashlib.sha256(data).hexdigest()}}}

if __name__=='__main__':
    WORK.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        result=list(pool.map(fetch,ASSETS))
    result.append(fetch_sunset())
    (WORK/'material-sources.json').write_text(json.dumps({'license_url':'https://polyhaven.com/license',
        'assets':result},indent=2)+'\n')
    print('Downloaded and verified',len(result),'selected material sets')
