# GROK — auto-post procedure (Buffer → TikTok + Instagram)

Used by the scheduled runs (3 per day) and by `/grok` when the user asks to post.
All times are Vietnam time (Asia/Ho_Chi_Minh, UTC+07:00).

## Schedule
- Scan + build: 07:00, 15:00, 23:00 (every 8 h), one video per run → 3 videos/day.
- Posting slots: **12:00, 19:00, 21:00**. Each video takes the **next free slot** after it is
  built (check both channels with `list_posts` first; a slot is taken if a post with the
  `GROK` caption is already scheduled there on that channel). Steady state: 23:00 build →
  12:00 next day, 07:00 build → 19:00, 15:00 build → 21:00.
- Only post a video whose Visual Critic verdict is **ACCEPTED**. If the critic rejects after
  fixes, post nothing and report why.

## Buffer
- Organization: "My Organization" `66f249d4ff57a3cad2a28053` (re-check with `get_account`).
- Channels (re-check with `list_channels`; never guess IDs):
  - TikTok `mr.pump395` — `6ae71290e29c69a17125bdd6`
  - Instagram `pumpmeme.crypto` (business) — `6ae71222e29c69a17125ba7a`
- `create_post` per channel: `schedulingType: "automatic"`, `mode: "customScheduled"`,
  `dueAt: "<YYYY-MM-DD>T<HH>:00:00+07:00"`, `assets: [{video: {url}}]`.
  - Instagram: `metadata.instagram = {type: "reel", shouldShareToFeed: true, isAiGenerated: true}`
  - TikTok: `metadata.tiktok = {isAiGenerated: true}`
- The video is AI-generated and the trades are simulated, so `isAiGenerated` is always true.

## Public video link (Buffer needs a direct, public download URL)
- Repo `nguyentv2912/octo-videos` (public), folder `grok/`. Attach with `add_repo`
  (access push), `git clone --depth 1`, copy the MP4 as
  `grok/grok_<YYYYMMDD>_<HHMM>_<HERO>.mp4`, commit (with the required attribution lines),
  `git fetch origin main && git rebase origin/main && git push origin main`.
- URL: `https://raw.githubusercontent.com/nguyentv2912/octo-videos/main/grok/<file>.mp4`.
  Check it returns HTTP 200 with `content-type` video/mp4 or application/octet-stream
  before creating posts. Only upload videos that will be posted (the repo is public).

## Caption (English)
```
GROK × MEME COIN — Road to $1M 🚀
Can an AI trading bot turn $<capital> into $<final equity> on $<HERO> and Solana memes?
Concept trades · Not financial advice
#solana #memecoin #crypto #grok #ai
```
- Line 2 is a question built from this video's numbers and hero token (vary the wording
  each run; never promise profits). Keep the disclaimer line.

## Report (Vietnamese)
Scan time, verified tokens (symbol, 24h %, volume), hero token, capital → final / P&L / ROI,
critic verdict, video link, and for each channel: slot (VN time), post id, status.
