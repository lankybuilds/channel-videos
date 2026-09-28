"""Forced-align the voiceover to the script with pocketsphinx; print word timings as JSON."""
import json, subprocess, sys
from pocketsphinx import Decoder

SCRIPT = ("more than half of new songs on deezer are made by ai "
          "january twenty twenty five ten thousand a day then thirty fifty sixty seventy five "
          "by june ninety thousand nine times in seventeen months but here's the twist "
          "half the uploads just one to three percent of streams almost nobody is listening "
          "the next hit might not have a heartbeat would you listen")

path = sys.argv[1]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                     capture_output=True, check=True).stdout
d = Decoder(samprate=16000, bestpath=False)
# words missing from the dictionary get approximate pronunciations
for w, pron in {'deezer': 'D IY Z ER', 'ai': 'EY AY', "here's": 'HH IH R Z'}.items():
    try:
        d.add_word(w, pron, True)
    except Exception as e:
        print('dict', w, e, file=sys.stderr)
d.set_align_text(SCRIPT)
d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
words = [{'w': s.word, 's': round(s.start_frame / 100, 3), 'e': round(s.end_frame / 100, 3)}
         for s in d.seg() if s.word not in ('<s>', '</s>', '<sil>')]
json.dump(words, open(sys.argv[2], 'w'), indent=0)
for x in words:
    print(f"{x['s']:6.2f} {x['e']:6.2f} {x['w']}")
