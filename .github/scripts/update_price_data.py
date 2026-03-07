import requests,csv,io,json,datetime

CSV_URL='https://online-price-watch.consumer.org.hk/opw/opendata/pricewatch_zh-Hant.csv'

def ymd(dt):
    return dt.strftime('%Y%m%d')

def build():
    now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    start=now-datetime.timedelta(days=7)
    end=now-datetime.timedelta(days=1)

    list_url=(
        'https://app.data.gov.hk/v1/historical-archive/list-file-versions'
        f'?url={CSV_URL}&start={ymd(start)}&end={ymd(end)}'
    )
    lj=requests.get(list_url,timeout=40).json()
    ts=lj['timestamps'][-1]
    get_url=(
        'https://app.data.gov.hk/v1/historical-archive/get-file'
        f'?url={CSV_URL}&time={ts}'
    )
    resp=requests.get(get_url,timeout=60)
    text=resp.content.decode('utf-8-sig',errors='replace')

    reader=csv.reader(io.StringIO(text))
    next(reader,None)
    rows=[]
    for r in reader:
        if len(r)<9:
            continue
        try:
            p=float(r[7])
        except:
            continue
        rows.append({
            'c1':r[0],'c2':r[1],'c3':r[2],'code':r[3],'brand':r[4],
            'name':r[5],'store':r[6],'price':p,'promo':r[8]
        })

    out={'timestamp':ts,'count':len(rows),'rows':rows}
    with open('price-data.json','w',encoding='utf-8') as f:
        json.dump(out,f,ensure_ascii=False,separators=(',',':'))
    print('updated',len(rows),ts)

if __name__ == '__main__':
    build()
