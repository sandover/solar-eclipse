(function() {
'use strict';
const $=id=>document.getElementById(id), clone=x=>JSON.parse(JSON.stringify(x));
const themes=JSON.parse($('payload').textContent), byId=Object.fromEntries(themes.map(t=>[t.id,t]));
const KEY='solar-eclipse-workshop-v1';
const labels={base03:'Page background',base02:'Raised surface / code backing',base01:'Comments / subdued text',base00:'Secondary text',base0:'Body text',base1:'Bright text',base2:'Pale neutral',base3:'Palest neutral',surround:'Surround / navigation',border:'Rules / table borders',h1:'H1 · title',h2:'H2 · section',h3:'H3 · subsection',h4:'H4 · detail',h5:'H5 · minor heading',h6:'H6 · source heading',link:'Links',bold:'Strong emphasis',italic:'Italic emphasis',inline:'Inline code text',quote:'Quotation',marker:'List markers',highlight:'Highlighted passage',selection:'Text selection',success:'Success / completed task',warning:'Warning / callout title',fn:'Functions',str:'Strings',meta:'Tags / special syntax',kw:'Keywords',num:'Numbers',ty:'Types / attributes',err:'Errors',sp:'Directives',heading1:'Code palette · title',heading2:'Code palette · section',bracket_olive:'Bracket accent'};
const priority=['base03','base0','surround','base02','h1','h2','h3','h4','h5','h6','link','bold','italic','inline','quote','marker','highlight','selection','border','success','warning'];
let state={version:1,theme:'candidate-verdigris-e',drafts:{},snapshots:[],view:{font:'sans',size:18,leading:1.65,width:70},sample:''};
let role='base0',mode='markdown',coords,opacity=1,saveTimer;
const status=message=>$('status').textContent=message;
function resolve(colors,key,seen=new Set()) {
  if(seen.has(key)||!colors[key])throw Error('Invalid color relationship: '+key);
  seen.add(key);return Color.valid(colors[key])?colors[key]:resolve(colors,colors[key],seen);
}
function validateDraft(d) {
  if(!d||!byId[d.theme]||!d.colors||!d.baseline)throw Error('Unknown starting point or missing palette.');
  const keys=Object.keys(byId[d.theme].colors);
  for(const palette of [d.colors,d.baseline]) {
    if(Object.keys(palette).length!==keys.length)throw Error('The palette has missing or extra roles.');
    for(const k of keys){if(typeof palette[k]!=='string'||(!Color.valid(palette[k])&&!keys.includes(palette[k])))throw Error('Invalid color for '+k);resolve(palette,k);}
    for(const k of ['base03','base0','surround'])if(resolve(palette,k).length!==7)throw Error('Page, body and surround must be opaque.');
  }
  if(d.notes!==undefined&&typeof d.notes!=='string')throw Error('Invalid notes.');
  return d;
}
function draft(){
  if(!state.drafts[state.theme])state.drafts[state.theme]={theme:state.theme,colors:clone(byId[state.theme].colors),baseline:clone(byId[state.theme].colors),notes:'',name:''};
  return state.drafts[state.theme];
}
function validateView(v){return v&&['sans','mono','serif','inconsolata','ibm-plex-sans','atkinson-hyperlegible'].includes(v.font)&&Number.isFinite(v.size)&&v.size>=14&&v.size<=24&&Number.isFinite(v.leading)&&v.leading>=1.3&&v.leading<=2&&Number.isFinite(v.width)&&v.width>=40&&v.width<=90;}
try {
  const saved=JSON.parse(localStorage.getItem(KEY)||'null');
  if(saved){
    if(saved.version!==1||!byId[saved.theme]||!validateView(saved.view)||typeof saved.sample!=='string'||!Array.isArray(saved.snapshots))throw Error('Invalid saved workspace.');
    Object.entries(saved.drafts).forEach(([id,d])=>{validateDraft(d);if(id!==d.theme)throw Error('Mismatched draft.');});
    saved.snapshots.forEach(s=>{validateDraft(s);if(typeof s.id!=='string'||typeof s.name!=='string')throw Error('Invalid snapshot.');});
    state=saved;status('Restored your browser workspace.');
  }
}catch(e){status('Could not restore browser storage. You can still tune and export a file.');}
function persist(){
  clearTimeout(saveTimer);saveTimer=null;
  try{localStorage.setItem(KEY,JSON.stringify(state));status('Draft saved in this browser. Export JSON to share it.');return true;}
  catch(e){status('Browser storage is unavailable or full. Export JSON to keep your work.');return false;}
}
const referenceUpgrade = upgradeReferences(state, themes);
if (referenceUpgrade.changed) {
  state = referenceUpgrade.state;
  if (persist()) status('Updated reading palettes loaded. Previous drafts are preserved as snapshots.');
}
function queueSave(){clearTimeout(saveTimer);saveTimer=setTimeout(persist,250);}
function option(select,value,text){const o=document.createElement('option');o.value=value;o.textContent=text;select.append(o);}
let group;
for(const t of themes){if(!group||group.label!==t.source){group=document.createElement('optgroup');group.label=t.source;$('theme').append(group);}option(group,t.id,t.label);option($('reference'),t.id,t.source+' · '+t.label);}
$('theme').value=state.theme;
for(const key of ['font','size','leading','width'])$(key).value=state.view[key];
$('sample').value=state.sample;
const axes=[['Lightness · L*',0,100,.1],['Chroma · C*',0,140,.1],['Hue · degrees',0,360,.1],['Opacity · %',0,100,1]];
axes.forEach(([label,min,max,step],i)=>{
  const div=document.createElement('div');div.className='axis';
  div.innerHTML=`<label for="axis${i}">${label}</label><input type="range" id="axis${i}" min="${min}" max="${max}" step="${step}"><input type="number" id="number${i}" aria-label="${label}" min="${min}" max="${max}" step="${step}">`;
  $('axes').append(div);
  for(const prefix of ['axis','number'])$(prefix+i).addEventListener('input',e=>{
    if(e.target.value===''||!e.target.validity.valid)return;
    const n=Number(e.target.value);if(i<3)coords[i]=n;else opacity=n/100;
    $('axis'+i).value=n;$('number'+i).value=n;
    const mapped=Color.fromLch(coords);
    draft().colors[role]=mapped.hex+(opacity<1?Math.round(opacity*255).toString(16).padStart(2,'0'):'');
    $('gamut').textContent=mapped.chroma<coords[1]-.05?`Outside sRGB: displayed chroma ${mapped.chroma.toFixed(1)} (requested ${coords[1].toFixed(1)}). Lightness and hue retained.`:'Within sRGB. Hue has little effect near zero chroma.';
    updateColor();
  });
});
function keys(){return [...priority,...Object.keys(draft().colors).filter(k=>!priority.includes(k))];}
function renderRoles(){
  const query=$('filter').value.toLowerCase();$('roles').replaceChildren();
  for(const k of keys()){
    if(!((labels[k]||k)+' '+k).toLowerCase().includes(query))continue;
    const b=document.createElement('button');b.className='role';b.dataset.key=k;b.setAttribute('aria-pressed',String(k===role));
    const chip=document.createElement('i');chip.style.background=resolve(draft().colors,k);
    const label=document.createElement('span');label.textContent=labels[k]||k;
    const hint=document.createElement('small');hint.textContent=draft().colors[k]!==draft().baseline[k]?'•':'';
    b.append(chip,label,hint);b.onclick=()=>selectRole(k);$('roles').append(b);
  }
  $('changed').textContent=Object.keys(draft().colors).filter(k=>draft().colors[k]!==draft().baseline[k]).length+' edited';
}
function requiresOpaque(k){
  return ['base03','base0','surround'].some(root=>{
    const seen=new Set();
    while(!seen.has(root)){
      if(root===k)return true;
      seen.add(root);
      if(Color.valid(draft().colors[root]))return false;
      root=draft().colors[root];
    }
    return false;
  });
}
function selectRole(k){
  role=k;const hex=resolve(draft().colors,role);coords=Color.toLch(hex);opacity=hex.length===9?parseInt(hex.slice(7),16)/255:1;
  $('roleTitle').textContent=labels[role]||role;
  [...coords,opacity*100].forEach((v,i)=>{for(const p of ['axis','number'])$(p+i).value=Number(v.toFixed(1));});
  const opaque=requiresOpaque(role);
  $('axis3').disabled=opaque;$('number3').disabled=opaque;
  $('gamut').textContent='Within sRGB. Hue has little effect near zero chroma.';
  $('linkRole').replaceChildren();option($('linkRole'),'','Independent color');
  for(const k of keys()){
    if(k===role)continue;
    try{const c={...draft().colors,[role]:k};resolve(c,role);if(opaque&&resolve(c,role).length!==7)continue;option($('linkRole'),k,labels[k]||k);}catch(e){}
  }
  updateColor(false);
}
function updateColor(save=true){
  const c=draft().colors,hex=resolve(c,role);$('hex').value=hex;$('hex').setCustomValidity('');$('picker').value=hex.slice(0,7);
  $('linkRole').value=Color.valid(c[role])?'':c[role];
  $('relationship').textContent=`${Color.contrast(hex,resolve(c,'base03')).toFixed(2)}:1 against the page. `+(Color.valid(c[role])?'Independent role.':`Follows ${labels[c[role]]||c[role]}; editing detaches it.`);
  renderRoles();paint();if(save)queueSave();
}
function setHex(hex){
  if(!Color.valid(hex)||(requiresOpaque(role)&&hex.length!==7)){$('hex').setCustomValidity('Use #RRGGBB (or #RRGGBBAA for transparent roles).');$('hex').reportValidity();return;}
  draft().colors[role]=hex.toLowerCase();selectRole(role);queueSave();
}
$('hex').onchange=()=>setHex($('hex').value.trim());$('picker').oninput=()=>setHex($('picker').value+(opacity<1?Math.round(opacity*255).toString(16).padStart(2,'0'):''));
$('linkRole').onchange=()=>{draft().colors[role]=$('linkRole').value||resolve(draft().colors,role);selectRole(role);queueSave();};
$('resetRole').onclick=()=>{const c={...draft().colors,[role]:draft().baseline[role]};try{Object.keys(c).forEach(k=>resolve(c,k));}catch(e){status('Reset would create a circular link. Remove the other link first.');return;}draft().colors=c;selectRole(role);queueSave();};
$('filter').oninput=renderRoles;
function preview(label,colors,editable,profileId){
  const section=document.createElement('section');section.className='preview';section.dataset.editable=editable;section.classList.toggle('solarized-reference', Boolean(byId[profileId]?.reference));
  const bar=document.createElement('div');bar.className='preview-label';
  const title=document.createElement('span');title.textContent=label;const stats=document.createElement('span');stats.className='stats';bar.append(title,stats);
  section.append(bar);const top=document.createElement('div');top.className='document-top';top.dataset.role='surround';top.textContent='Journal / A quieter place to think';section.append(top);
  const paper=document.createElement('div');paper.className='paper';paper.dataset.role='base03';
  const doc=document.createElement('article');doc.className='document';doc.dataset.role='base0';
  if(mode==='markdown')doc.innerHTML=Examples.markdown;
  else {const pre=document.createElement('pre');pre.className='source';pre.innerHTML=Examples[mode];doc.append(pre);}
  const sample=document.createElement('p');sample.className='user-sample';sample.textContent=state.sample;doc.append(sample);
  paper.append(doc);section.append(paper);section._colors=colors;
  section.addEventListener('click',e=>{if(e.target.closest('a'))e.preventDefault();if(!editable)return;const hit=e.target.closest('[data-role]');if(hit){selectRole(hit.dataset.role);$('roleTitle').scrollIntoView({block:'nearest',behavior:'smooth'});}});
  return section;
}
function renderPreviews(){
  const compare=$('compare').checked;$('comparisonOptions').hidden=!compare;$('previews').classList.toggle('comparing',compare);$('previews').replaceChildren();
  $('previews').append(preview('Your draft',draft().colors,true,state.theme));
  if(compare){const ref=$('reference').value;const snapshot=state.snapshots.find(s=>'snapshot:'+s.id===ref);const c=ref==='baseline'?draft().baseline:snapshot?snapshot.colors:byId[ref].colors;const label=ref==='baseline'?'Starting point':snapshot?snapshot.name:byId[ref].source+' · '+byId[ref].label;$('previews').append(preview(label,c,false,ref==='baseline'?state.theme:snapshot?snapshot.theme:ref));}
  paint();
}
function paint(){
  for(const el of document.querySelectorAll('.preview')){
    const c=el.dataset.editable==='true'?draft().colors:el._colors;
    Object.keys(c).forEach(k=>el.style.setProperty('--'+k,resolve(c,k)));
    const fonts={inconsolata:'"Inconsolata", monospace','ibm-plex-sans':'"IBM Plex Sans", sans-serif','atkinson-hyperlegible':'"Atkinson Hyperlegible", sans-serif',sans:'system-ui, sans-serif',mono:'"Inconsolata", ui-monospace, monospace',serif:'Georgia, serif'};
    el.style.setProperty('--font',fonts[state.view.font]);el.style.setProperty('--size',state.view.size+'px');el.style.setProperty('--leading',state.view.leading);el.style.setProperty('--width',state.view.width+'ch');
    el.querySelector('.stats').textContent='Body '+Color.contrast(resolve(c,'base0'),resolve(c,'base03')).toFixed(2)+':1';
    el.querySelectorAll('[data-role]').forEach(n=>{const k=n.dataset.role;if(!['base03','surround','base02','highlight'].includes(k))n.style.color=resolve(c,k);});
    el.querySelector('.user-sample').textContent=state.sample;
  }
}
function loadTheme(){
  $('theme').value=state.theme;$('provenance').textContent=byId[state.theme].description || byId[state.theme].source+' · browser approximation of reading and syntax roles; not an exact app renderer.';
  $('notes').value=draft().notes||'';$('saveName').value=draft().name||'';
  if(!draft().colors[role])role='base0';renderPreviews();selectRole(role);
}
$('theme').onchange=()=>{state.theme=$('theme').value;loadTheme();persist();};
for(const b of document.querySelectorAll('[data-mode]'))b.onclick=()=>{mode=b.dataset.mode;document.querySelectorAll('[data-mode]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));renderPreviews();};
$('compare').onchange=renderPreviews;$('reference').onchange=renderPreviews;
for(const key of ['font','size','leading','width'])$(key).oninput=()=>{state.view[key]=key==='font'?$(key).value:Number($(key).value);paint();queueSave();};
$('sample').oninput=()=>{state.sample=$('sample').value;paint();queueSave();};
$('notes').oninput=()=>{draft().notes=$('notes').value;queueSave();};$('saveName').oninput=()=>{draft().name=$('saveName').value;queueSave();};
function packageDraft(){return {format:'solar-eclipse-palette',version:1,...clone(draft()),name:$('saveName').value.trim()||byId[state.theme].label+' exploration',source:byId[state.theme].source,savedAt:new Date().toISOString(),view:clone(state.view),sample:state.sample,resolved:Object.fromEntries(Object.keys(draft().colors).map(k=>[k,resolve(draft().colors,k)]))};}
function listSnapshots(){const selected=$('snapshots').value;$('snapshots').replaceChildren();option($('snapshots'),'','Choose a saved snapshot…');for(const s of state.snapshots)option($('snapshots'),s.id,s.name+' · '+new Date(s.savedAt).toLocaleString());$('snapshots').value=selected;
  const ref=$('reference').value;
  $('reference').querySelectorAll('[data-snapshot]').forEach(o=>o.remove());
  for(const s of state.snapshots){option($('reference'),'snapshot:'+s.id,'Saved · '+s.name);$('reference').lastElementChild.dataset.snapshot='true';}
  $('reference').value=[...$('reference').options].some(o=>o.value===ref)?ref:'baseline';
  if($('compare').checked)renderPreviews();
}
$('save').onclick=()=>{const s={...packageDraft(),id:crypto.randomUUID?crypto.randomUUID():String(Date.now())};state.snapshots.push(s);const stored=persist();listSnapshots();$('snapshots').value=s.id;if(stored)status('Snapshot saved: '+s.name+'. Export JSON for a portable copy.');};
$('restore').onclick=()=>{const s=state.snapshots.find(x=>x.id===$('snapshots').value);if(!s){status('Choose a snapshot first.');return;}state.theme=s.theme;state.drafts[s.theme]=clone(s);if(validateView(s.view))state.view=clone(s.view);state.sample=s.sample||'';for(const k of ['font','size','leading','width'])$(k).value=state.view[k];$('sample').value=state.sample;loadTheme();persist();};
$('delete').onclick=()=>{const s=state.snapshots.find(x=>x.id===$('snapshots').value);if(!s)return;if(!confirm('Delete saved snapshot “'+s.name+'”? Your current draft stays.'))return;state.snapshots=state.snapshots.filter(x=>x.id!==s.id);listSnapshots();persist();};
$('resetTheme').onclick=()=>{if(!confirm('Reset this draft to its starting palette? Saved snapshots stay.'))return;draft().colors=clone(draft().baseline);loadTheme();persist();};
$('export').onclick=()=>{const data=packageDraft(),blob=new Blob([JSON.stringify(data,null,2)+'\n'],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=data.theme+'-'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status('Exported this complete palette, baseline, notes, and reading conditions.');};
$('copy').onclick=async()=>{const s=packageDraft();const changes=Object.keys(s.colors).filter(k=>s.colors[k]!==s.baseline[k]);const text=[s.name,s.source+' / '+s.theme,s.notes,'',`Body ${resolve(s.colors,'base0')} on ${resolve(s.colors,'base03')}`,`Reading: ${s.view.font}, ${s.view.size}px, line spacing ${s.view.leading}, width ${s.view.width}ch`,'',...changes.map(k=>`${labels[k]||k} (${k}): ${resolve(s.baseline,k)} → ${resolve(s.colors,k)}${Color.valid(s.colors[k])?'':' (follows '+s.colors[k]+')'}`)].join('\n');try{await navigator.clipboard.writeText(text);status('Copied your notes and changed colors.');}catch(e){status('Clipboard unavailable here. Export JSON instead.');}};
$('import').onclick=()=>$('importFile').click();
$('importFile').onchange=async()=>{const file=$('importFile').files[0];if(!file)return;try{if(file.size>1000000)throw Error('File is too large.');const s=JSON.parse(await file.text());if(s.format!=='solar-eclipse-palette'||s.version!==1||!validateView(s.view)||typeof s.sample!=='string')throw Error('Expected a Solar Eclipse palette export.');validateDraft(s);const snapshot={...s,id:crypto.randomUUID?crypto.randomUUID():String(Date.now()),name:typeof s.name==='string'?s.name:'Imported palette',savedAt:new Date().toISOString()};state.snapshots.push(snapshot);listSnapshots();$('snapshots').value=snapshot.id;const stored=persist();if(stored)status('Imported as a snapshot. Click Load to explore it; your draft has not changed.');}catch(e){status('Import failed: '+e.message);}finally{$('importFile').value='';}};
window.addEventListener('pagehide',()=>{if(saveTimer)persist();});
loadTheme();listSnapshots();
})();
