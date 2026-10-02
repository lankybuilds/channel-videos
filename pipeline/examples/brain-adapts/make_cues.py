import json
w = json.load(open('words_rt.json'))
OFF = 0.3
def T(word, n=1, after=0.0):
    k = 0
    for x in w:
        if x['w'] == word and x['s'] + OFF >= after:
            k += 1
            if k == n: return round(x['s'] + OFF, 3)
    raise KeyError(word)
def E(word, n=1, after=0.0):
    k = 0
    for x in w:
        if x['w'] == word and x['s'] + OFF >= after:
            k += 1
            if k == n: return round(x['e'] + OFF, 3)
C = {'vo_offset': OFF}
C['h1'] = 0.25
C['h2'] = T('can') - 0.03
C['slam'] = T('anything') - 0.02
C['kids'] = T('some') - 0.05
C['half'] = T('half') - 0.03
C['removed'] = T('removed')
C['years'] = T('years') - 0.03
C['runs'] = T('runs') - 0.05
C['network'] = T('network')
C['cut1'] = T('blind') - 0.15
C['blind'] = T('blind')
C['dots'] = [T('braille'), E('readers', 1, C['blind']) - 0.1]
C['vision'] = T('vision') - 0.05
C['lights'] = T('lights')
C['finger'] = T('through') - 0.03
C['cut2'] = T('london') - 0.15
C['london'] = T('london')
C['map'] = [T('memorize') - 0.1, T('twenty')]
C['count'] = [T('twenty'), T('streets')]
C['streets'] = T('streets')
C['memory'] = T('their', 1, C['streets']) - 0.03
C['grows'] = T('grows')
C['cut3'] = T('some', 2) - 0.15
C['some'] = T('some', 2)
C['gifted'] = T('born') - 0.03
C['but'] = T('but') - 0.03
C['rewires'] = T('rewires') - 0.03
C['whatever'] = T('whatever') - 0.03
C['practice'] = T('practice') - 0.02
C['remember'] = T('remember') - 0.05
C['ybj'] = T('your', 2, C['remember']) - 0.03 if False else T('your', 1, C['remember']) - 0.03
C['phys'] = T('physically') - 0.03
C['changed'] = T('changed') - 0.02
C['dur'] = round(w[-1]['e'] + OFF + 1.5, 2)
C = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in C.items()}
json.dump(C, open('cues.json', 'w'))
print(json.dumps(C))
