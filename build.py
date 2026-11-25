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
wkp=os.path.join(root,'data','weeks.json')
wk=js(json.load(open(wkp,encoding='utf-8'))) if os.path.exists(wkp) else '{}'
html=re.sub(r'/\*__WK__\*/.*?/\*__ENDWK__\*/',lambda m:wk,html,flags=re.S)
wmp=os.path.join(root,'data','weeks_meta.json')
wm=js(json.load(open(wmp,encoding='utf-8'))) if os.path.exists(wmp) else '{}'
html=re.sub(r'/\*__WM__\*/.*?/\*__ENDWM__\*/',lambda m:wm,html,flags=re.S)
# Identifiants publics Firebase (facultatif) : sans ce fichier, la page reste en mode local hors de claude.ai.
fbp=os.path.join(root,'firebase-config.json')
fb=js(json.load(open(fbp,encoding='utf-8'))) if os.path.exists(fbp) else 'null'
html=re.sub(r'/\*__FB__\*/.*?/\*__ENDFB__\*/',lambda m:fb,html,flags=re.S)
open(os.path.join(root,'artifact.html'),'w',encoding='utf-8').write(html)
# Version autonome (document complet) pour un hébergement classique comme Vercel.
shell='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'
open(os.path.join(root,'index.html'),'w',encoding='utf-8').write(shell+html+'</body></html>')
print(len(html),{k:len(v) for k,v in data.items()},len(cat))
