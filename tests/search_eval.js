/* Runs the site search engine (assets/search/engine.js) in node for tests/test_search_queries.py.
   node tests/search_eval.js <engine.js> <index dir>  < [[lang, query], ...]  ->  [[url, ...] top 5 per query, ...]
   An older search.js with the engine inside (before engine.js) runs too: in a stub page, with one line before its closing
   "})();" that hands out its find() and load(). */
const fs = require('fs'), path = require('path'), vm = require('vm');
const [js, dir] = process.argv.slice(2);
const src = fs.readFileSync(js, 'utf8');
const queries = JSON.parse(fs.readFileSync(0, 'utf8'));

async function engine(lang) {
  const data = JSON.parse(fs.readFileSync(path.join(dir, `${lang}.json`), 'utf8'));
  if (src.includes('gabellaSearchEngine =')) {
    const ctx = {};
    vm.runInNewContext(src, ctx);
    return ctx.gabellaSearchEngine(lang, data);
  }
  const btn = { getAttribute: () => '', setAttribute() {}, querySelector: () => null, addEventListener() {} };
  const ctx = {
    document: { currentScript: { dataset: { root: '' }, src: 'search.js' }, querySelector: s => (s === '.srchbtn' ? btn : null), documentElement: { lang } },
    navigator: { platform: '', userAgent: '', onLine: true }, addEventListener() {}, setTimeout, clearTimeout,
    fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve(data) }),
  };
  vm.runInNewContext(src.replace(/\}\)\(\);\s*$/, 'globalThis.__eng = { find, load };\n})();'), ctx);
  await ctx.__eng.load();
  return ctx.__eng;
}

(async () => {
  const engines = {}, out = [];
  for (const [lang, q] of queries) {
    const e = engines[lang] || (engines[lang] = await engine(lang));
    out.push(e.find(q).slice(0, 5).map(it => it.u));
  }
  process.stdout.write(JSON.stringify(out));
})();
