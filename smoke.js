// Test de fumée : exécute le script de la page avec un DOM factice.
const fs=require('fs');const html=fs.readFileSync(process.argv[2],'utf8');
const js=html.slice(html.lastIndexOf('<script>')+8,html.lastIndexOf('</script>'));
const els={};const mk=id=>els[id]||(els[id]={id,innerHTML:'',hidden:false,open:false,addEventListener(){},close(){},showModal(){},textContent:''});
const handlers={};
global.document={getElementById:mk,addEventListener:(t,f)=>handlers[t]=f,activeElement:null};
const mem={};global.localStorage={getItem:k=>k in mem?mem[k]:null,setItem:(k,v)=>mem[k]=String(v)};
global.window={};
const run=new Function(js+`;return {ui,render,recommend,Store,slots,whenTxt,booking,week,handlers:null,save,weekPath,availOf,CATS,PRESET,NB}`);
const A=run();
setTimeout(()=>{
  const out=[];const {ui}=A;
  out.push('mode='+A.Store.mode+' ready='+A.Store.ready+' week='+ui.week);
  for(const club of ['auteuil','beaugrenelle']){
    A.save('group/settings',{club});
    const sl=A.slots();out.push(club+': slots='+sl.length+' sansCat='+sl.filter(s=>!s.cat).length+' idsUniques='+(new Set(sl.map(s=>s.id)).size===sl.length));
    const r=A.recommend();
    r.plans.forEach((p,i)=>out.push('  plan'+i+' '+p.sc.toFixed(2)+' | '+A.CATS.map(([c])=>A.whenTxt(p.pick[c].s)+' '+p.pick[c].s.course+' n'+p.pick[c].n+' ['+A.booking(p.pick[c].s).txt+']').join(' | ')));
  }
  A.save('group/settings',{club:'auteuil'});
  for(const t of ['semaine','planning','dispos','idees']){ui.tab=t;A.render();out.push(t+': '+els.app.innerHTML.length+' car.')}
  // choisir un plan, réserver, places, dispo perso, veto
  const click=(d)=>handlers.click({target:{closest:()=>({dataset:d,tagName:'BUTTON'})}});
  ui.tab='semaine';click({act:'choose',i:'0'});
  const plan=A.week().plan;out.push('plan choisi='+JSON.stringify(plan));
  click({act:'book',id:plan.force,p:'p1'});click({act:'places',id:plan.cardio,v:'0'});
  out.push('booked='+JSON.stringify(A.week().booked)+' places='+JSON.stringify(A.week().places));
  const r2=A.recommend();out.push('cardio complet exclu='+!r2.by.cardio.some(x=>x.s.id===plan.cardio));
  click({act:'pref',c:'RPM',v:'0'});ui.edit='p1';
  out.push('veto RPM p1 -> RPM à 3 restant='+A.recommend().by.cardio.filter(x=>x.s.course==='RPM'&&x.n===3).length);
  ui.scope='week';click({act:'cell',d:'0',b:'0'});out.push('dispo perso semaine='+A.availOf('p1').custom+' a[0]='+A.availOf('p1').a[0]);
  click({act:'resetweek'});out.push('retour semaine type='+!A.availOf('p1').custom);
  click({act:'slot',id:plan.force});out.push('dialogue: '+els.dlg.innerHTML.length+' car.');
  click({act:'clearplan'});out.push('plan effacé='+(A.week().plan===undefined));
  ui.week='2026-11-23';A.render();out.push('semaine en cours rendue ok');
  console.log(out.join('\n'));
},50);
