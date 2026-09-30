import json
w = json.load(open('words_rt.json'))
OFF = 0.3
def find(word, n=1, after=0.0):
    k = 0
    for x in w:
        if x['w'] == word and x['s'] >= after:
            k += 1
            if k == n: return round(x['s'] + OFF, 3)
    raise KeyError(word)
T = lambda word, n=1, after=0.0: find(word, n, after - OFF if after else 0)
C = {'vo_offset': OFF}
C['s1b'] = T('socially') - 0.05
C['s1c'] = T('might') - 0.1
C['s1d'] = T('stay') - 0.05
C['cut2'] = T("here's") - 0.15
C['m1'] = T('not', 1, C['cut2']) - 0.05
C['ne1'] = T('adhd', 1, C['m1'])
C['m2'] = T('being', 1, C['ne1']) - 0.05
C['ne2'] = T('autistic', 1, C['m2'])
C['m3'] = T('everyone') - 0.05
C['cut3'] = T('social', 1, C['m3']) - 0.15
C['c52'] = T('researchers')
C['p52'] = T('half', 1, C['c52'])
C['c27'] = T('only', 1, C['p52']) - 0.05
C['p27'] = T('quarter', 1, C['c27'])
C['cut4'] = T('adhd', 1, C['p27']) - 0.15
C['slash4'] = T("it's", 1, C['cut4']) - 0.25
C['a1'] = T('time', 1, C['cut4'])
C['a2'] = T('start', 1, C['a1']) - 0.3
C['a3'] = T('emotions', 1, C['a2'])
C['a4'] = T('childhood', 1, C['a3']) - 0.3
C['cut5'] = T('autism', 1, C['a4']) - 0.15
C['slash5'] = T("it's", 1, C['cut5']) - 0.25
C['b1'] = T('sensory', 1, C['cut5'])
C['b2'] = T('masking', 1, C['b1'])
C['b3'] = T('exhaustion', 1, C['b2'])
C['b4'] = T('looks', 1, C['b3']) - 0.2
C['cut6'] = T('these', 1, C['b4']) - 0.15
C['c42'] = T('high', 1, C['cut6']) - 0.1
C['p42'] = T('anxiety', 1, C['c42'])
C['c37'] = C['p42'] + 0.35
C['p37'] = T('depression', 1, C['p42'])
C['c79'] = T('even', 1, C['p37']) - 0.1
C['p79'] = T('lives', 1, C['c79'])
C['cut7'] = T('so', 1, C['p79']) - 0.15
C['dont'] = T('you', 1, C['cut7'] + 1.2) - 0.03   # "You DON'T" (the you after the beat)
C['n1'] = T('not', 1, C['dont'])
C['pro'] = T('only', 1, C['n1'])
C['fin'] = T('if', 1, C['pro'])
C['dur'] = round(w[-1]['e'] + OFF + 1.6, 2)
C = {k: round(v, 3) for k, v in C.items()}
json.dump(C, open('cues.json', 'w'))
print(json.dumps(C))
