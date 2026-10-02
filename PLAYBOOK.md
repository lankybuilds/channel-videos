# Daily video playbook

The daily scheduled run follows this file. Keep it up to date when the owner gives new feedback.

## Hard rules (from the owner)
- Never use emojis, anywhere: on screen, in captions, scripts or titles.
- No blinking typewriter cursor. Letter-by-letter spell-out is fine without one.
- Pure black and white (#000 / #FFF), minimalist kinetic typography. Fonts: Anton (headlines), JetBrains Mono (labels, sources).
- About 4 scenes, one idea each, one thing animating at a time. Text stays still long enough to read, but keep gaps between scenes short: the voice drives the timing.
- Only one inverted (white) scene per video, at the key reveal. At most 3 transitions.
- Safe area: nothing important in the top 200 px or bottom 300 px. Thin progress bar at the bottom. Loop cleanly.
- Every number fact-checked with web search against a primary or reputable source, with the arithmetic run in code. Source line on screen. Never overstate a stat (say which platform or country, and when).

## Topics
Alternate days: tech/AI in numbers, then general mind-blowing facts (science, history, the body, big-number comparisons). Vary the format (surge/growth chart, myth-bust, scale comparison, "how it works") so the channel doesn't look mass-produced. Check `topics.md` to avoid repeats, and add each new topic there.

## Topic approval (shorts, before any voice generation)
- After picking and fact-checking the topic, message the owner a pitch: the topic, the angle/format, the key facts with sources, and the draft script. Then stop and wait.
- Generate the voice only after the owner approves the idea. If they reject it, pitch a different topic (same category rules) and wait again. Never spend ElevenLabs credits on an unapproved idea.

## Voice (ElevenLabs connector)
- Voice "Mike - Social Media, Narrator, Clean", voice_id E4aVOlWL5DGbFy7TWmZA, model eleven_v3, generations_count 1 (ONE take only: the owner wants to save credits).
- Create one flow per video (creative_create_flow), named "<date> - <topic>".
- Script: 55-70 words (about 25-28 s after trimming pauses), 2-9 word sentences, numbers spelled out in words, CAPS on 1-2 emphasis words, a varied eleven_v3 tag at the start of each line ([dramatic], [building excitement], [impressed], [whispering], [intrigued], [serious], [curious]...).
- The workspace cannot download from ElevenLabs. Once the idea is approved and the take is generated, message the owner the flow link, and ask them to attach the take as an MP3 (or ask for a redo if they dislike it).

## Build (after the MP3 arrives)
Work in a scratch folder with `OUT=<folder>`. Copy in `pipeline/`, then:
1. `pip install --break-system-packages pocketsphinx`, then `npm pack @fontsource/anton @fontsource/jetbrains-mono` and unpack into `fonts/` (see build.py for the paths).
2. `python3 align.py vo_raw.mp3 script.txt words.json`. Add missing words to the dictionary block if alignment fails.
3. Trim long pauses as retime.py does (edit its cap() rules for the new take): about 0.28 s inside lists, 0.35-0.5 s at scene changes, up to 0.7 s for one dramatic beat. Writes vo.mp3 + words_rt.json.
4. Write a new template.html for this video's scenes (reuse the helpers and structure from the existing one: CUES object, enter/slam/withScale, camera drift, progress bar, renderAt). Derive cues.json from word times (text lands on the first syllable of its word, cuts about 0.1-0.2 s before the new line, vo_offset 0.3).
5. Write build_events() in sfx.py for this video's moments (slams, whooshes on cuts, plucks and ticks for counts, power-down + drone into the inverted scene, etc.). Synth only, no music. Keep slams at 0.55-0.6 and the fx master at 0.5 so the voice stays on top.
6. `python3 build.py audio`, `html`, `sheet <times>` (look at the contact sheet: layout, safe area, sync), then `video`. Master to about -14 LUFS (volume +5 dB, alimiter, loudnorm, as in the first video).
7. Commit the MP4 to `videos/YYYY-MM-DD-slug.mp4` and push to main.

## Post (Metricool connector, blogId 7123535, timezone America/Los_Angeles)
- createScheduledPost with media = `https://raw.githubusercontent.com/lankybuilds/channel-videos/main/videos/<file>.mp4`
- providers instagram (instagramData type REEL, showReelOnFeed true, isAiGenerated true) and tiktok (tiktokData title required, privacyOption PUBLIC_TO_EVERYONE, isAigc true).
- Time: 10:00 AM today. If it's already past about 9:45 AM, use 6:00 PM today, or 10:00 AM tomorrow if that has passed too.
- Caption: 2-3 short lines (hook, question for comments, "Source: ..."), then 5-6 relevant hashtags. No emojis.
- Send the owner the planner link, time and caption when done.

## Long-form essays (YouTube, 1920x1080)
Same hard rules as above, adapted to landscape. Reference build: `pipeline/essay/` (first essay, 2026-09-28).
- Script 650-800 words, eleven_v3 Mike voice, one take (about 4,900 credits; fits one request under 5,000 characters).
- `scenes.py` defines ~30 scenes; every element is timed to a word (`W(line, 'word')`) from the aligned lines. At most 3 wipes (chapter starts), one inverted scene, chapter label top-left, source line bottom-left, chapter ticks on the progress bar.
- `retime_essay.py` caps: 0.32 s inside lines, 0.6 s between lines, 0.85 s before beats, 1.1 s at chapter starts (keeps it over 4 minutes).
- Render with `render_seg.py` in parallel segments of 1,000-1,500 frames (a single long background render gets killed), concat, mux mix.mp3, then volume + alimiter to about -14 LUFS.
- Commit to `videos/essays/YYYY-MM-DD-slug.mp4` and log in `essay-topics.md`.
