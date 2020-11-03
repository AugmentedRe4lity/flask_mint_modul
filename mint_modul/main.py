from flask import Flask, render_template, request, redirect, make_response
from db_manager import init_db, add_to_db, get_db_tables, get_db_data
from datetime import datetime, date


app = Flask(__name__)


@app.route('/', methods = ['POST', 'GET'])
def index():
    global mysql
    cd = request.cookies.get('l') if request.cookies.get('l')!=None else ''
    try:
        name = request.args.get('name')
        da = request.args.get('date').replace(',', '.')+'.2020'
        uz = request.args.get('uz').replace(',','.')
        uz = uz if not uz == '' else None
        ort = request.args.get('G').replace(',', '.')
        temp = request.args.get('temperatur').replace(',', '.')
        temp = int(temp) if len(temp)>0 and temp!='-' else None
        nitrat = request.args.get('nitrat').replace(',', '.')
        nitrat = int(nitrat) if len(nitrat)>0 and nitrat!='-' else None
        nwl = request.args.get('nwl').replace(',', '.')
        nwl = float(nwl) if len(nwl)>0 and nwl!='-' else None
        nitrit = request.args.get('nitrit').replace(',', '.')
        nitrit = float(nitrit) if len(nitrit)>0 and nitrit!='-' else None
        niwl = request.args.get('niwl').replace(',', '.')
        niwl = float(niwl) if len(niwl)>0 and niwl!='-' else None
        ammo = request.args.get('ammonium').replace(',', '.')
        ammo = float(ammo) if len(ammo)>0 and ammo!='-' else None
        awl = request.args.get('awl').replace(',', '.')
        awl = float(awl) if len(awl)>0 and awl!='-' else None
        phos = request.args.get('phosphat').replace(',', '.')
        phos = float(phos) if len(phos)>0 and phos!='-' else None
        pwl = request.args.get('pwl').replace(',', '.')
        pwl = float(pwl) if len(pwl)>0 and pwl!='-' else None
        ph = request.args.get('phwert').replace(',', '.')
        ph = float(ph) if len(ph)>0 and ph!='-' else None
        gpsx = request.args.get('gpsx').replace(',','.')
        gpsx = float(gpsx) if len(gpsx)>0 and gpsx!='-' else None
        gpsy = request.args.get('gpsy').replace(',','.')
        gpsy = float(gpsy) if len(gpsy)>0 and gpsy!='-' else None
        l = [da, uz, ort, temp, nitrat, nwl, nitrit, niwl, ammo, awl, phos, pwl, ph, gpsx, gpsy]
        if request.args.get('send')=='send':
            init_db(l[0])
            add_to_db(l)

            f = open('log.txt', 'a')
            f.write(';'.join([str(da),str(uz), str(ort), str(temp), str(nitrat), str(nwl), str(nitrit), str(niwl), str(ammo), str(awl), str(phos), str(pwl), str(ph),str(gpsx),str(gpsy)])+'\t'+name+'\n')
            f.close()

    except:
        pass

    dat = date.today()
    dat = str(dat)
    dat = dat[-2:]+'.'+dat[-5:-3]
    if request.args.get('url') != None:
        link = request.args.get('url')
        resp = make_response(render_template('main.html', date=dat, link=link))
    else:
        resp = make_response(render_template('main.html', date=dat, link='static/images.jpg'))

    try:
        resp.set_cookie('l', cd+' '.join([str(i) for i in l])+'\n')
        print(True, '; '.join([str(i) for i in l]))
    except:
        pass
    return resp

@app.route('/down')
def download():
    return render_template('data.csv')

@app.route('/viewer')
def viewer():
    with open('templates/data.csv', 'r') as f:
        t = f.read().split('\n')
    for i in range(len(t)):
        t[i] = t[i].split(',')
    d = []
    for e in t:
        if e[0] not in d:
            if e[0]!="":
                d.append(e[0])
    print(d[1:], d[1:-1])
    d = d[1:]
    return render_template('viewer.html', d=d)

@app.route('/tables', methods=['POST', 'GET'])
def tables():
    f = open('templates/data.csv', 'r')
    t = f.read()
    f.close()
    t = t.split('\n')[:-1]
    for i in range(len(t)):
        t[i] = t[i].split(',')
    da = request.args.get('date')
    content1 = []
    for i, e in enumerate(t):
        if e[0]==da:
            content1.append(t[i])
    content = []
    for i, gb in enumerate(['GB1', 'GB2', 'GB3', 'GB4', 'GB5']):
        for e in content1:
            if str(e[1]).strip()==str(gb).strip() and str(e[1]).strip() not in [l[1] for l in content]:
                content.append(e)
            else:
                for j, v in enumerate(e):
                    if v.strip()!='' and v.strip()!='-':
                        if content[len(content)-1][j].strip()=='' or content[len(content)-1][j].strip()=='':
                            content[len(content)-1][j]=v
    for i in range(len(content), 5):
        content.append(['-','-','-','-','-','-','-','-','-','-','-'])
    return render_template('tables.html', content=content)

@app.route('/cookiedata')
def cookiedata():
    cd = request.cookies.get('l') if request.cookies.get('l')!=None else ''
    l = cd.split('\n')
    for i in range(len(l)):
        l[i] = l[i].split(' ')
    print(l)
    return render_template('cookie_data.html', l=l)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port='8081')
