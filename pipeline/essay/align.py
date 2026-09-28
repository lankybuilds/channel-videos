"""Forced-align the voiceover to the script with pocketsphinx; print word timings as JSON."""
import json, re, subprocess, sys
from pocketsphinx import Decoder


# usage: python3 align.py vo.mp3 script.txt words.json
path = sys.argv[1]
SCRIPT = re.sub(r"[^a-z' ]", ' ', re.sub(r'\[[^\]]*\]', ' ', open(sys.argv[2]).read().lower()))
SCRIPT = ' '.join(SCRIPT.split())
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     capture_output=True, check=True).stdout
d = Decoder(samprate=16000, bestpath=False)
# words missing from the dictionary get approximate pronunciations
for w, pron in {'ai': 'EY AY', 'chatgpt': 'CH AE T JH IY P IY T IY', 'freelanced': 'F R IY L AE N S T', 'gpt': 'JH IY P IY T IY', "shopify's": 'SH AA P IH F AY Z'}.items():
    try:
        d.add_word(w, pron, True)
    except Exception as e:
        print('dict', w, e, file=sys.stderr)
d.set_align_text(SCRIPT)
d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
words = [{'w': s.word, 's': round(s.start_frame / 100, 3), 'e': round(s.end_frame / 100, 3)}
         for s in d.seg() if s.word not in ('<s>', '</s>', '<sil>')]
json.dump(words, open(sys.argv[3], 'w'), indent=0)
for x in words:
    print(f"{x['s']:6.2f} {x['e']:6.2f} {x['w']}")
