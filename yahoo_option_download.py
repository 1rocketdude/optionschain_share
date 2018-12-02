#!/usr/local/bin/python3

import datetime as dt
import requests
import sys
import json

''' yengst@gmail.com Thomas St. Yeng
    created 2018-12-01
    
    download all the option data for a single symbol from Yahoo. Put them in the current directory as json files.
    
'''


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('%s SYMBOL' % sys.argv[0])
        sys.exit(1)
    
    symbol = sys.argv[1].upper()
    url_base = 'https://query1.finance.yahoo.com/v7/finance/options/%s' % symbol

    print(url_base)
    try:
        r = requests.get(url_base, timeout=20)
        full = json.loads(r.text)
    except:
        print('%s could not decode FIRST Yahoo options chain JSON content' % symbol)
        with open('%s underlying.json' % symbol,'wt') as f: print(r.text,file=f)
        sys.exit(1)
        
    if full['optionChain']['error'] is None:
        opt = full['optionChain']['result'][0]
        del opt['strikes']
    else:
        print('%s returned error %s' % (symbol,full['optionChain']['error']))
        sys.exit(1)
            
    for this_expiration in opt['expirationDates'][1:]:
        this_dt_str = str(dt.date.fromtimestamp(this_expiration))
        url = url_base + '?date=%s' % this_expiration
        try:
            r = requests.get(url, timeout=20)
            full = json.loads(r.text)
            print('\texpiry %s' % this_dt_str)
        except:
            print('\tfailed to get %s' % this_dt_str)
            with open('%s %s.json' % (symbol,this_dt_str),'wt') as f: print(r.text,file=f)
            continue
        
        if full['optionChain']['error'] is None:
            opt['options'].append(full['optionChain']['result'][0]['options'][0])
    
    with open('%s %s.json' % (symbol,str(dt.date.today())),'wt') as f: json.dump(opt,f)
    