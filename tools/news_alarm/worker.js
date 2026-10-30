// Alarm of the news automation. Every 10 minutes starts
//   gabella-wow/wow          news-auto.yml  (watcher of Blizzard, short note on the site; public repo, free minutes)
// every 30 minutes starts
//   gabella-wow/gabella-bot  news.yml       (the same notes to Discord; private repo, Actions minutes are limited)
// GitHub's own cron is late by hours. The token lives only in the Worker secret GH_DISPATCH_TOKEN
// (fine-grained, these two repositories only, Actions: read and write). The workflows decide by their switches
// (variables NEWS_AUTO / NEWS_DISCORD): the alarm sends no mode.
const SITE = 'https://api.github.com/repos/gabella-wow/wow/actions/workflows/news-auto.yml/dispatches';
const BOT = 'https://api.github.com/repos/gabella-wow/gabella-bot/actions/workflows/news.yml/dispatches';

async function dispatch(env, withBot) {
  const out = [];
  for (const url of withBot ? [SITE, BOT] : [SITE]) {
    const r = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.GH_DISPATCH_TOKEN}`,
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'gabella-news-alarm',
      },
      body: JSON.stringify({ ref: 'main' }),
    });
    console.log(`dispatch ${url.split('/')[5]}: ${r.status}`);   // 204 = started; 401/403 = token; 404 = workflow not on main yet
    out.push(r.status);
  }
  return out;
}

export default {
  async scheduled(event, env, ctx) {
    const minute = new Date(event.scheduledTime).getUTCMinutes();
    ctx.waitUntil(dispatch(env, minute < 10 || minute >= 30 && minute < 40));
  },
  async fetch() {                        // no workers.dev address (workers_dev = false); this only answers that it is alive
    return new Response('gabella news alarm\n', { headers: { 'content-type': 'text/plain' } });
  },
};
