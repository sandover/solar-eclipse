/* Preserve old experiments before replacing a corrected reference baseline. */
(function(root) {
  function upgradeReferences(state, profiles) {
    const next = JSON.parse(JSON.stringify(state));
    const same = (a,b) => Object.keys(b).every(k => a[k] === b[k]);
    let changed = false;
    for (const profile of profiles.filter(p => p.reference || p.revision)) {
      const draft = next.drafts[profile.id];
      if (!draft || same(draft.baseline, profile.colors)) continue;
      next.snapshots.push({
        ...draft, id: 'reference-upgrade-' + profile.id + '-' + Date.now(),
        name: (draft.name || profile.label) + ' · before palette revision',
        savedAt: new Date().toISOString(), view: {...next.view}, sample: next.sample
      });
      next.drafts[profile.id] = {
        theme: profile.id, colors: {...profile.colors}, baseline: {...profile.colors},
        notes: '', name: ''
      };
      changed = true;
    }
    return {state: next, changed};
  }
  root.upgradeReferences = upgradeReferences;
})(typeof module === 'object' ? module.exports : window);
