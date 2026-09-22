/* CIELAB D65, matching utils/pal.py. Chroma is reduced at the sRGB boundary. */
(function(root) {
  const linear = x => { x /= 255; return x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4; };
  const gamma = x => x <= .0031308 ? 12.92 * x : 1.055 * x ** (1 / 2.4) - .055;
  const f = x => x > 216/24389 ? Math.cbrt(x) : 841/108*x + 4/29;
  const inv = x => x**3 > 216/24389 ? x**3 : (x-4/29)*108/841;
  const bytes = hex => [1,3,5].map(i => parseInt(hex.slice(i,i+2),16));
  const valid = hex => /^#[0-9a-f]{6}([0-9a-f]{2})?$/i.test(hex);
  function toLch(hex) {
    const [r,g,b] = bytes(hex).map(linear);
    const x=f((r*.4124564+g*.3575761+b*.1804375)/.95047);
    const y=f(r*.2126729+g*.7151522+b*.0721750);
    const z=f((r*.0193339+g*.1191920+b*.9503041)/1.08883);
    const a=500*(x-y), bb=200*(y-z);
    return [116*y-16,Math.hypot(a,bb),(Math.atan2(bb,a)*180/Math.PI+360)%360];
  }
  function rgb([L,C,h]) {
    const t=h*Math.PI/180,y=(L+16)/116;
    const x=inv(y+C*Math.cos(t)/500)*.95047, yy=inv(y), z=inv(y-C*Math.sin(t)/200)*1.08883;
    return [x*3.2404542-yy*1.5371385-z*.4985314,-x*.969266+yy*1.8760108+z*.041556,x*.0556434-yy*.2040259+z*1.0572252].map(gamma);
  }
  const inGamut = v => v.every(x => x >= -.0001 && x <= 1.0001);
  function fromLch([L,C,h]) {
    let actual=C;
    if (!inGamut(rgb([L,C,h]))) {
      let low=0,high=C;
      for(let i=0;i<40;i++){const mid=(low+high)/2;if(inGamut(rgb([L,mid,h])))low=mid;else high=mid;}
      actual=low;
    }
    return {hex:'#'+rgb([L,actual,h]).map(v=>Math.round(Math.max(0,Math.min(1,v))*255).toString(16).padStart(2,'0')).join(''),chroma:actual};
  }
  function composite(fg,bg) {
    const a=fg.length===9?parseInt(fg.slice(7),16)/255:1;
    return '#'+bytes(fg).map((x,i)=>Math.round(x*a+bytes(bg)[i]*(1-a)).toString(16).padStart(2,'0')).join('');
  }
  function luminance(h){const [r,g,b]=bytes(h).map(linear);return r*.2126729+g*.7151522+b*.072175;}
  function contrast(a,b){const x=luminance(composite(a,b)),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
  root.Color={toLch,fromLch,valid,contrast,composite};
})(typeof module==='object'?module.exports:window);
