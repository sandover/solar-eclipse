window.Examples = {
markdown: `
<div class="doc-meta" data-role="base00">FIELD NOTES / 21 SEPTEMBER 2026</div>
<h1 data-role="h1">A quieter place to think</h1>
<p>Good tools leave room for the work. A page should help us follow an idea through its turns: a question, a small discovery, a decision worth keeping. Most of our time is spent here, in ordinary sentences, rather than in titles.</p>
<p>The goal is <strong data-role="bold">steady attention</strong>. Color can mark a change of subject without interrupting the thought. We want something <em data-role="italic">distinctive enough to enjoy</em> and familiar enough to disappear.</p>
<h2 data-role="h2">What we learned this week</h2>
<p>We compared the morning notes with the longer afternoon draft. The useful distinction was between <a href="#" data-role="link">finding a passage</a> and reading it closely. Both should feel natural on the same page.</p>
<h3 data-role="h3">Keep the foundation quiet</h3>
<p>Read this paragraph slowly. Look away, then return. Do the letters settle into the ground, or seem to hover above it? A color that feels pleasing in a small swatch can feel insistent across an entire page.</p>
<ul><li>Keep enough distinction between the page and its surrounding panels.</li><li>Let headings make the outline easy to scan.<ul><li>Use fewer competing signals within each paragraph.</li><li>Give repeated details a consistent visual role.</li></ul></li><li>Try a longer reading session before deciding.</li></ul>
<blockquote data-role="quote">“The details are not the details. They make the design.”<br><small>— Charles Eames</small></blockquote>
<h3 data-role="h3">Make the next step clear</h3>
<p>Save a version before changing the background. The setting <code data-role="inline">reading.width</code> should support a comfortable line length. <mark data-role="highlight">A highlight should help us return to an idea</mark>, without taking over the whole paragraph.</p>
<div class="callout" data-role="base02"><strong data-role="warning">A note for later</strong><p>Compare the colors together, with the same typeface and the same text. Measurements can explain a difference; your reading experience decides whether it helps.</p></div>
<h4 data-role="h4">Review checklist</h4>
<ul class="tasks"><li><span data-role="success">☑</span> Read a page of uninterrupted prose</li><li><span data-role="marker">☐</span> Check links, inline code, and quotations</li><li><span data-role="marker">☐</span> Revisit the palette in evening light</li></ul>
<table><thead><tr><th>Element</th><th>Purpose</th><th>Question</th></tr></thead><tbody><tr><td>Body text</td><td>Sustained reading</td><td>Does it feel effortless?</td></tr><tr><td>Headings</td><td>Orientation</td><td>Can I find my place?</td></tr><tr><td>Accents</td><td>Meaning</td><td>Do they belong together?</td></tr></tbody></table>
<h5 data-role="h5">A small observation</h5><p>Not every detail needs a new color. Repetition can make a page feel considered.</p>
<h6 data-role="h6">Source note</h6><p class="footnote" data-role="base00">Working notes, revision 03. See <a href="#" data-role="link">the reading journal</a> for earlier comparisons.</p><hr>
<h2 data-role="h2">Tomorrow’s work</h2><ol><li>Choose a complete palette to live with.</li><li>Keep a short note about what still feels distracting.</li><li>Return with fresh eyes.</li></ol>`,
source: `<span data-role="base01">#</span> <span data-role="h1">A quieter place to think</span>

Good tools leave room for the work. A page should help us follow
an idea through its turns: a question, a small discovery,
a decision worth keeping.

<span data-role="base01">##</span> <span data-role="h2">What we learned this week</span>

The goal is <span data-role="bold">**steady attention**</span>, with enough character to make
reading <span data-role="italic">*a pleasure*</span>. See <span data-role="link">[the reading journal](./journal.md)</span>.

<span data-role="base01">###</span> <span data-role="h3">Keep the foundation quiet</span>

<span data-role="marker">-</span> Let headings make the outline easy to scan.
<span data-role="marker">-</span> Keep repeated details consistent.
  <span data-role="marker">-</span> Check links and <span data-role="inline">\x60reading.width\x60</span> in context.

<span data-role="quote">&gt; Compare complete palettes, not isolated swatches.</span>

<span data-role="success">- [x]</span> Read a full page of prose
<span data-role="marker">- [ ]</span> Revisit in evening light

<span data-role="base01">####</span> <span data-role="h4">Review checklist</span>
<span data-role="base01">#####</span> <span data-role="h5">A small observation</span>
<span data-role="base01">######</span> <span data-role="h6">Source note</span>

| Element   | Purpose           |
|-----------|-------------------|
| Body text | Sustained reading |
| Headings  | Orientation       |`,
code: `<span data-role="base01">// Keep a reading session small enough to return to.</span>
<span data-role="kw">import</span> { <span data-role="ty">readFile</span> } <span data-role="kw">from</span> <span data-role="str">'node:fs/promises'</span>;

<span data-role="kw">interface</span> <span data-role="ty">ReadingNote</span> {
  <span data-role="ty">title</span>: <span data-role="ty">string</span>;
  <span data-role="ty">minutes</span>: <span data-role="ty">number</span>;
  <span data-role="ty">tags</span>: <span data-role="ty">string</span>[];
}

<span data-role="kw">export async function</span> <span data-role="fn">loadJournal</span>(path: <span data-role="ty">string</span>) {
  <span data-role="kw">const</span> source = <span data-role="kw">await</span> <span data-role="fn">readFile</span>(path, <span data-role="str">'utf8'</span>);
  <span data-role="kw">const</span> notes: <span data-role="ty">ReadingNote</span>[] = <span data-role="meta">JSON</span>.<span data-role="fn">parse</span>(source);
  <span data-role="kw">return</span> notes.<span data-role="fn">filter</span>(note =&gt; note.minutes &gt; <span data-role="num">15</span>);
}

<span data-role="kw">const</span> session = {
  <span data-role="ty">title</span>: <span data-role="str">'An ordinary afternoon'</span>,
  <span data-role="ty">minutes</span>: <span data-role="num">25</span>,
  <span data-role="ty">tags</span>: [<span data-role="str">'draft'</span>, <span data-role="str">'reading'</span>],
};

<span data-role="base01">// HTML and CSS put different pressures on a palette.</span>
&lt;<span data-role="meta">article</span> <span data-role="ty">class</span>=<span data-role="str">"reading-note"</span>&gt;
  &lt;<span data-role="meta">h1</span>&gt;An ordinary afternoon&lt;/<span data-role="meta">h1</span>&gt;
&lt;/<span data-role="meta">article</span>&gt;

<span data-role="sp">@media</span> (min-width: <span data-role="num">48rem</span>) {
  <span data-role="meta">.reading-note</span> {
    <span data-role="ty">max-width</span>: <span data-role="num">70ch</span>;
    <span data-role="ty">color</span>: <span data-role="fn">var</span>(--body-text);
  }
}

<span data-role="err">Error: journal.md could not be read.</span>
<span data-role="warning">Warning: one note has no title.</span>
<span data-role="success">Saved 12 notes.</span>`
};
