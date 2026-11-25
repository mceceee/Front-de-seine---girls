import json,re,sys,os
root=os.path.dirname(os.path.abspath(__file__))
days=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
data={}
for club in ['auteuil','beaugrenelle']:
    rows=json.load(open(os.path.join(root,'data',club+'.json')))
    out=[]
    for r in rows:
        t,coach=r['time'],r['coach']
        # Coquille du PDF : TRX Auteuil vendredi, un « 9h30 » imprimé après 18h30.
        if club=='auteuil' and r['studio']=='TRX Studio' and r['day']=='vendredi' and t=='09:30' and coach=='Antony.A':
            t='19:45'; coach='Antony.A · horaire à confirmer (imprimé 9h30)'
        out.append([r['studio'],days.index(r['day']),t,r['course'],coach])
    data[club]=out
cat={c['course']:{'dur':c['duration_min'],'max':c['max_participants']} for c in json.load(open(os.path.join(root,'data','catalogue.json')))}
js=lambda o: json.dumps(o,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
html=open(os.path.join(root,'head.html'),encoding='utf-8').read()+open(os.path.join(root,'script.html'),encoding='utf-8').read()
html=re.sub(r'/\*__DATA__\*/.*?/\*__ENDDATA__\*/',lambda m:js(data),html,flags=re.S)
html=re.sub(r'/\*__CAT__\*/.*?/\*__ENDCAT__\*/',lambda m:js(cat),html,flags=re.S)
open(os.path.join(root,'index.html'),'w',encoding='utf-8').write(html)
print(len(html),{k:len(v) for k,v in data.items()},len(cat))
