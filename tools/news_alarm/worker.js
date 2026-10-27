// Alarm of the news watcher: every 10 minutes starts the workflow news-auto of RaiGanja/wow (GitHub's own cron is late by hours).
// The token lives only in the Worker secret GH_DISPATCH_TOKEN (fine-grained, RaiGanja/wow only, Actions: read and write).
// The workflow itself decides by the repository variable NEWS_AUTO (on/off): the alarm sends no mode.
const URL = 'https://api.github.com/repos/RaiGanja/wow/actions/workflows/news-auto.yml/dispatches';

async function dispatch(env) {
  const r = await fetch(URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.GH_DISPATCH_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'gabella-news-alarm',
    },
    body: JSON.stringify({ ref: 'main' }),
  });
  console.log(`dispatch: ${r.status}`);   // 204 = started; 401/403 = token; 404 = workflow not on main yet
  return r.status;
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(dispatch(env));
  },
  async fetch() {                        // the workers.dev address answers only that it is alive, it starts nothing
    return new Response('gabella news alarm\n', { headers: { 'content-type': 'text/plain' } });
  },
};
