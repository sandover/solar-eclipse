const {test}=require('node:test');
const assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const {Color}=require('../review/color.js');
const fs=require('node:fs');
const html=fs.readFileSync('index.html','utf8');
const profiles=JSON.parse(html.match(/<script id="payload" type="application\/json">(.*?)<\/script>/s)[1]);
const hexes=[...new Set(profiles.flatMap(p=>Object.values(p.colors).filter(Color.valid).map(h=>h.slice(0,7))))];
test('all generated colors round-trip through D65 Lab without changing an RGB byte',()=>{
  for(const hex of [...hexes,'#000000','#ffffff','#ff0000','#00ff00','#0000ff'])assert.equal(Color.fromLch(Color.toLch(hex)).hex,hex);
});
test('browser color science matches the Python palette tools, including gamut boundaries',()=>{
  const inputs=[[55,8,110],[60,18,235],[50,140,90],[10,120,310],[95,60,180],[0,140,1],[100,140,359]];
  const python=JSON.parse(execFileSync('python3',['-c',`import sys,json,contextlib,io;sys.path.insert(0,'utils');\nwith contextlib.redirect_stdout(io.StringIO()): from pal import lch2hex\nprint(json.dumps([lch2hex(x) for x in json.loads(sys.argv[1])]))`,JSON.stringify(inputs)],{encoding:'utf8'}));
  inputs.forEach((input,i)=>{const actual=Color.fromLch(input);assert.equal(actual.hex,python[i][0]);assert.ok(Math.abs(actual.chroma-python[i][1])<.001);});
});
test('contrast handles transparent overlays on their actual ground',()=>{
  assert.ok(Math.abs(Color.contrast('#ffffff','#000000')-21)<.001);
  assert.equal(Color.contrast('#ffffff00','#123456'),1);
  assert.equal(Color.composite('#ffffff80','#000000'),'#808080');
});
test('every profile has a complete, acyclic set of preview roles',()=>{
  function resolve(c,k,seen=[]){assert.ok(!seen.includes(k),'cycle '+k);assert.equal(typeof c[k],'string');return Color.valid(c[k])?c[k]:resolve(c,c[k],[...seen,k]);}
  assert.equal(profiles.length,21);
  for(const p of profiles){for(const k of Object.keys(p.colors))assert.ok(Color.valid(resolve(p.colors,k)));for(const k of ['base0','base03','h1','h2','h3','link','selection','surround'])assert.ok(resolve(p.colors,k));}
});

test('Solarized Green preserves the reference lightness ladder and accents',()=>{
  const reference=profiles.find(p=>p.id==='shared-solarized').colors;
  const green=profiles.find(p=>p.id==='candidate-solarized-green').colors;
  for(const key of ['base03','base02','base01','base00','base0','base1'])
    assert.ok(Math.abs(Color.toLch(reference[key])[0]-Color.toLch(green[key])[0])<.2);
  for(const key of ['base2','base3','fn','str','meta','kw','num','ty','err','sp'])
    assert.equal(green[key],reference[key]);
  assert.ok(Math.abs(Color.contrast(reference.base0,reference.base03)-Color.contrast(green.base0,green.base03))<.05);
});

test('Solarized reference matches the published palette and VS Code Markdown scopes',()=>{
  const ref=JSON.parse(fs.readFileSync('references/solarized-dark.json','utf8'));
  assert.deepEqual(Object.values(ref.palette),[
    '#002b36','#073642','#586e75','#657b83','#839496','#93a1a1','#eee8d5','#fdf6e3',
    '#b58900','#cb4b16','#dc322f','#d33682','#6c71c4','#268bd2','#2aa198','#859900'
  ]);
  for(const id of ['reference-vscode-solarized']){
    const c=profiles.find(p=>p.id===id).colors;
    const theme=JSON.parse(fs.readFileSync('references/vscode-solarized-dark.json','utf8'));
    function token(scope){let value;for(const rule of theme.tokenColors){const scopes=Array.isArray(rule.scope)?rule.scope:[rule.scope];if(scopes.includes(scope)&&rule.settings.foreground)value=rule.settings.foreground.toLowerCase();}return value;}
    const scopes={h1:'markup.heading',h2:'markup.heading',h3:'markup.heading',h4:'markup.heading',h5:'markup.heading',h6:'markup.heading',bold:'markup.bold',italic:'markup.italic',inline:'markup.inline.raw',quote:'markup.quote',marker:'markup.list',link:'string'};
    for(const [role,scope] of Object.entries(scopes))assert.equal(c[c[role]],token(scope));
    assert.equal(c.selection,theme.colors['editor.selectionBackground']);
  }
});
test('corrected references preserve prior drafts, notes, and unrelated work',()=>{
  const {upgradeReferences}=require('../review/reference-upgrade.js');
  const profile=profiles.find(p=>p.id==='shared-solarized');
  const old={...profile.colors,h2:'str',h3:'fn'};
  const original={theme:profile.id,drafts:{[profile.id]:{theme:profile.id,colors:{...old,base0:'#999999'},baseline:old,notes:'Keep this experiment'},other:{colors:{x:'#123456'}}},snapshots:[],view:{font:'inconsolata'},sample:'My text'};
  const result=upgradeReferences(original,profiles);
  assert.equal(result.changed,true);
  assert.equal(result.state.snapshots[0].colors.base0,'#999999');
  assert.equal(result.state.snapshots[0].notes,'Keep this experiment');
  assert.equal(result.state.snapshots[0].sample,'My text');
  assert.deepEqual(result.state.drafts[profile.id].colors,profile.colors);
  assert.deepEqual(result.state.drafts.other,original.drafts.other);
  assert.equal(original.snapshots.length,0);
  assert.equal(upgradeReferences(result.state,profiles).changed,false);
});

test('every local Markdown profile has a reading design, separate from the reference',()=>{
  for(const p of profiles.filter(p=>!p.reference)) {
    assert.ok(p.revision, p.id);
    assert.equal(p.colors.italic,p.colors.base0,p.id);
    assert.equal(p.colors.quote,p.colors.base0,p.id);
  }
  const reading=profiles.find(p=>p.id==='shared-solarized');
  const reference=profiles.find(p=>p.id==='reference-vscode-solarized');
  assert.equal(reading.colors.base03,reference.colors.base03);
  assert.equal(reading.colors.base0,reference.colors.base0);
  assert.notEqual(reading.colors.h1,reference.colors.h1);
  assert.ok(!reading.reference);
});
