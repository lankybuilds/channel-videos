"""Scene spec for the long-form essay. Builds cues.json (absolute times) from lines.json word timings.
Every visible element lands on the first syllable of the word it belongs to."""
import json, re

L = json.load(open('lines.json'))
OFF = 0.3          # vo_offset
LEAD = 0.03        # text lands just before the syllable
CX = 960


def W(li, word=None, nth=0):
    """absolute time of a word in line li (first word if word is None)"""
    ws = L[li]['words']
    if word is None:
        return round(ws[0]['s'] + OFF - LEAD, 3)
    hits = [x for x in ws if x['w'] == word]
    assert len(hits) > nth, (li, word, [x['w'] for x in ws])
    return round(hits[nth]['s'] + OFF - LEAD, 3)


def E(li):
    return round(L[li]['e'] + OFF, 3)


def txt(t, text, x=CX, y=540, px=150, fam='H', align='center', anim='enter', maxW=1640, alpha=1.0, sfx=None):
    return dict(k='txt', t=t, text=text, x=x, y=y, px=px, fam=fam, align=align, anim=anim, maxW=maxW, alpha=alpha,
                sfx=sfx)


def count(t, a, b, x=CX, y=540, px=220, d=0.9, pre='', suf='', dec=0, align='center', maxW=1640, sfx='count'):
    return dict(k='count', t=t, a=a, b=b, x=x, y=y, px=px, d=d, pre=pre, suf=suf, dec=dec, align=align, maxW=maxW,
                sfx=sfx)


def bar(t, x, y, w, h, frac, d=0.6, sfx='pluck', note=0):
    return dict(k='bar', t=t, x=x, y=y, w=w, h=h, frac=frac, d=d, sfx=sfx, note=note)


def strike(t, x1, x2, y, sfx='strike'):
    return dict(k='strike', t=t, x1=x1, x2=x2, y=y, sfx=sfx)


def rule(t, x, y, w, sfx=None):
    return dict(k='rule', t=t, x=x, y=y, w=w, sfx=sfx)


S = []   # scenes


def scene(first_line, els, last=None, chap=None, src=None, trans='cut', inv=False):
    S.append(dict(start=round(W(first_line) - 0.15, 3), els=els, chap=chap, src=src, trans=trans, inv=inv))


C1, C2, C3, C4 = ('01 / WHAT IT USED TO TAKE', '02 / THE RECORD NUMBERS', '03 / THE AI MULTIPLIER',
                  '04 / THE HONEST PART')

# ---------------- INTRO ----------------
scene(0, [
    txt(W(0), 'EVERY HEADLINE. EVERY DAY.', y=250, px=40, fam='M', alpha=0.7, sfx='tick'),
    txt(W(1, 'money'), 'MONEY IS TIGHT.', y=470, px=150, sfx='hit'),
    txt(W(1, 'jobs'), 'JOBS ARE SHAKY.', y=660, px=150, sfx='hit'),
    txt(W(1, 'game'), 'THE GAME IS RIGGED.', y=850, px=150, sfx='hit'),
])
scene(2, [
    txt(W(2), 'MAKING MONEY HAS NEVER BEEN', y=400, px=96),
    txt(W(2, 'harder'), 'HARDER.', y=680, px=280, anim='slam', sfx='slam'),
    txt(W(2, 'right'), 'Right?', y=820, px=44, fam='M', alpha=0.8, sfx='tick'),
    strike(W(3, 'nobody'), 700, 1220, 590),
    txt(W(3, 'nobody'), 'Here is what nobody tells you.', y=900, px=44, fam='M', sfx=None),
])
scene(4, [
    txt(W(4), 'BY THE NUMBERS, STARTING TO EARN HAS NEVER BEEN', y=330, px=64),
    txt(W(4, 'easier'), 'EASIER.', y=640, px=330, anim='slam', sfx='slam'),
    txt(W(5, 'not'), 'Not effortless.', y=800, px=48, fam='M', alpha=0.7, sfx='tick'),
    txt(W(5, 'but'), 'But easier than at any point in history.', y=870, px=48, fam='M', sfx='tick'),
    txt(W(6), 'LET ME SHOW YOU THE NUMBERS.', y=960, px=30, fam='M', alpha=0.55, sfx=None),
])

# ---------------- 01 WHAT IT USED TO TAKE ----------------
scene(7, [
    txt(W(7), 'FIRST: WHAT IT USED TO TAKE.', y=300, px=110),
    txt(W(8), 'TO SELL SOMETHING,', y=500, px=90),
    txt(W(8, 'you'), 'YOU NEEDED A STOREFRONT.', y=620, px=90),
    txt(W(9, 'lease'), 'A LEASE', x=400, y=840, px=96, sfx='pluck0'),
    txt(W(9, 'inventory'), 'INVENTORY', x=960, y=840, px=96, sfx='pluck1'),
    txt(W(9, 'bank'), 'A BANK LOAN', x=1520, y=840, px=96, sfx='pluck2'),
], chap=C1, trans='wipe')
scene(10, [
    txt(W(10, 'publish'), 'PUBLISH A BOOK?', x=200, y=380, px=120, align='left'),
    txt(W(10, 'publisher'), 'A PUBLISHER HAD TO SAY YES.', x=1720, y=380, px=46, fam='M', align='right', sfx='tick'),
    txt(W(11, 'be'), 'BE ON TV?', x=200, y=600, px=120, align='left'),
    txt(W(11, 'network'), 'A NETWORK HAD TO SAY YES.', x=1720, y=600, px=46, fam='M', align='right', sfx='tick'),
    rule(W(12) - 0.1, 200, 700, 1520),
    txt(W(12), 'SOMEONE ALWAYS HELD THE GATE.', y=880, px=130, anim='slam', sfx='slam'),
], chap=C1)
scene(13, [
    txt(W(13, 'who'), 'WHO COULD YOU REACH?', y=230, px=100),
    dict(k='dots', t=W(13, 'who') + 0.2, x=CX, y=560, cols=25, rows=4, gap=62, r=14,
         steps=[[W(14, 'one'), 16], [W(15, 'six'), 75]], sfx='dots'),
    txt(W(14), '2005', x=520, y=790, px=60, fam='M', alpha=0.7, sfx=None),
    count(W(14, 'one'), 0, 1, x=520, y=920, px=110, d=0.6, suf=' BILLION ONLINE'),
    txt(W(15), '2025', x=1400, y=790, px=60, fam='M', alpha=0.7, sfx=None),
    count(W(15, 'six'), 1, 6, x=1400, y=920, px=110, d=0.7, suf=' BILLION'),
    txt(W(16), 'THREE QUARTERS OF EVERYONE ON EARTH.', y=380, px=46, fam='M', sfx='tick'),
], chap=C1, src='Source: ITU (2005 via McKinsey; Facts and Figures 2025). 1 dot = 1% of humanity.')
scene(17, [
    txt(W(17), 'YOUR POTENTIAL AUDIENCE.', y=470, px=170, anim='slam', sfx='slam'),
    txt(W(17, 'from'), 'From your phone.', y=620, px=56, fam='M', sfx='tick'),
], chap=C1)
scene(18, [
    txt(W(18), 'THEN', x=520, y=260, px=48, fam='M', alpha=0.6, sfx=None),
    txt(W(18), 'LEASE', x=520, y=420, px=100, alpha=0.8, sfx=None),
    txt(W(18), 'INVENTORY', x=520, y=540, px=100, alpha=0.8, sfx=None),
    txt(W(18), 'LOAN', x=520, y=660, px=100, alpha=0.8, sfx=None),
    txt(W(19), 'NOW', x=1400, y=260, px=48, fam='M', alpha=0.6, sfx=None),
    txt(W(19, 'five'), '$5', x=1400, y=600, px=330, anim='slam', sfx='slam'),
    txt(W(19, 'month'), 'A MONTH (Shopify Starter plan)', x=1400, y=700, px=36, fam='M', sfx='tick'),
    txt(W(20, 'cheaper'), 'CHEAPER THAN LUNCH.', y=880, px=110, sfx='hit'),
], chap=C1, src='Source: Shopify pricing, 2026.')

# ---------------- 02 THE RECORD NUMBERS ----------------
scene(21, [
    txt(W(21), 'SO ARE PEOPLE ACTUALLY USING THIS?', y=420, px=100),
    txt(W(22), 'YES.', y=720, px=300, anim='slam', sfx='slam'),
    txt(W(22, 'in'), 'In record numbers.', y=860, px=52, fam='M', sfx='tick'),
], chap=C2, trans='wipe')
scene(23, [
    txt(W(23), 'NEW BUSINESS APPLICATIONS, UNITED STATES', y=210, px=34, fam='M', alpha=0.7, sfx=None),
    rule(W(23), 260, 860, 1400),
    txt(W(23, 'nineteen'), '2019', x=660, y=920, px=40, fam='M', sfx=None),
    bar(W(23, 'three'), 520, 860, 280, 460, 3.5 / 5.5, d=0.7, note=0),
    count(W(23, 'three'), 0, 3.5, x=660, y=860 - 460 * 3.5 / 5.5 - 30, px=90, d=0.7, suf='M', dec=1, sfx=None),
    txt(W(24), '2023', x=1260, y=920, px=40, fam='M', sfx=None),
    bar(W(24, 'five'), 1120, 860, 280, 460, 1.0, d=0.8, note=4),
    count(W(24, 'five'), 0, 5.5, x=1260, y=860 - 460 - 30, px=90, d=0.8, suf='M', dec=1, sfx=None),
    txt(W(25), 'ALL-TIME RECORD', x=1560, y=320, px=60, align='left', maxW=330, sfx='hit'),
], chap=C2, src='Source: U.S. Census Bureau Business Formation Statistics, via Economic Innovation Group.')
scene(26, [
    txt(W(26), 'FREELANCING', y=250, px=44, fam='M', alpha=0.7, sfx='tick'),
    count(W(27, 'sixty'), 0, 64, y=520, px=260, d=0.9, suf=' MILLION'),
    txt(W(27, 'americans'), 'AMERICANS FREELANCED IN 2023', y=640, px=48, fam='M', sfx=None),
    txt(W(28, 'earned'), 'EARNING ABOUT', y=780, px=40, fam='M', alpha=0.7, sfx=None),
    count(W(28, 'one'), 0, 1.27, y=920, px=130, d=0.9, pre='$', suf=' TRILLION', dec=2),
], chap=C2, src='Source: Upwork, Freelance Forward 2023.')
scene(29, [
    txt(W(29, 'creators'), 'AND CREATORS?', y=260, px=90),
    count(W(30, 'one'), 0, 100, y=580, px=300, d=0.9, pre='$', suf='B+'),
    txt(W(30, 'in'), 'PAID OUT BY YOUTUBE IN FOUR YEARS', y=700, px=46, fam='M', sfx=None),
    txt(W(31), 'to creators, artists and media companies', y=770, px=36, fam='M', alpha=0.6, sfx=None),
    txt(W(32), 'A CAREER THAT BARELY EXISTED 20 YEARS AGO.', y=920, px=76, sfx='hit'),
], chap=C2, src='Source: YouTube, September 2025.')

# ---------------- 03 THE AI MULTIPLIER ----------------
scene(33, [
    txt(W(33), 'BUT HERE IS WHERE IT GETS WILD.', y=380, px=90),
    txt(W(34), 'ARTIFICIAL', y=640, px=230, anim='slam', sfx='slam'),
    txt(W(34, 'intelligence'), 'INTELLIGENCE.', y=860, px=230, anim='slam', sfx='hit'),
], chap=C3, trans='wipe')
scene(35, [
    txt(W(35, 'idea'), 'AN IDEA', x=200, y=330, px=120, align='left'),
    txt(W(35, 'cheap'), 'WAS CHEAP.', x=1720, y=330, px=120, align='right', sfx='hit'),
    txt(W(36), 'MAKING IT REAL', x=200, y=520, px=120, align='left'),
    txt(W(36, 'expensive'), 'WAS EXPENSIVE.', x=1720, y=520, px=120, align='right', sfx='hit'),
    dict(k='boxes', t=[W(37, 'coder'), W(37, 'designer'), W(37, 'writer'), W(37, 'team')],
         labels=['CODER', 'DESIGNER', 'WRITER', 'TEAM'], merge=W(38, 'one'), y=780, sfx='boxes'),
    txt(W(38, 'one'), 'ONE PERSON.', y=820, px=130, anim='slam', sfx='slam'),
], chap=C3)
scene(39, [
    txt(W(39, 'idea'), 'AN IDEA FOR AN APP.', y=250, px=110),
    txt(W(40), 'TEN YEARS AGO', x=200, y=450, px=44, fam='M', align='left', alpha=0.7, sfx=None),
    bar(W(40, 'hired'), 200, 530, 1520, 60, 1.0, d=1.4, sfx='long'),
    txt(W(40, 'hired'), 'Hire developers. Wait months.', x=200, y=640, px=44, fam='M', align='left', sfx=None),
    txt(W(41), 'TODAY', x=200, y=740, px=44, fam='M', align='left', alpha=0.7, sfx=None),
    bar(W(41, 'describe'), 200, 770, 1520, 60, 0.08, d=0.3, sfx='pluck', note=5),
    txt(W(41, 'describe'), 'Describe it in plain English.', x=200, y=900, px=44, fam='M', align='left', sfx=None),
    txt(W(41, 'ai'), 'AI HELPS WRITE THE CODE.', x=1720, y=900, px=56, align='right', sfx='hit'),
], chap=C3)
scene(42, [
    txt(W(42, 'logo'), 'A LOGO', x=200, y=300, px=110, align='left'),
    txt(W(42, 'minutes'), 'MINUTES', x=1720, y=300, px=110, align='right', sfx='pluck0'),
    txt(W(43), 'WEBSITE. PHOTOS. AN AD. A SCRIPT.', x=200, y=480, px=90, align='left', maxW=1000),
    txt(W(44, 'afternoon'), 'AN AFTERNOON', x=1720, y=480, px=90, align='right', maxW=560, sfx='pluck2'),
    txt(W(45), 'A WEEK OF RESEARCH', x=200, y=720, px=110, align='left'),
    txt(W(45, 'summarized'), 'SUMMARIZED', x=1720, y=720, px=110, align='right', sfx='pluck4'),
    txt(W(45, 'coffee'), 'before your coffee cools.', x=1720, y=790, px=40, fam='M', align='right', sfx=None),
    txt(W(44), 'First drafts, not a quarter.', x=200, y=550, px=34, fam='M', align='left', alpha=0.6, sfx=None),
], chap=C3)
scene(46, [
    dict(k='wave', t=W(46), y=420, sfx=None),
    txt(W(46, 'voice'), 'THIS VOICE?', y=700, px=150),
    txt(W(46, 'made'), 'MADE WITH AI.', y=880, px=150, anim='slam', sfx='slam'),
], chap=C3)
scene(47, [
    txt(W(47, 'not'), 'NOT HYPE.', y=420, px=200, sfx='hit'),
    txt(W(47, 'measured'), 'MEASURED.', y=720, px=260, anim='slam', sfx='slam'),
], chap=C3)
scene(48, [
    txt(W(48), 'EXPERIMENT: DEVELOPERS + AI CODING ASSISTANT', y=220, px=34, fam='M', alpha=0.7, sfx=None),
    txt(W(48, 'web'), 'BUILD A WEB SERVER.', y=340, px=90),
    txt(W(48, 'web'), 'WITHOUT AI', x=200, y=470, px=36, fam='M', align='left', alpha=0.7, sfx=None),
    bar(W(48, 'web') + 0.3, 200, 510, 1520, 70, 1.0, d=1.0, sfx='long'),
    txt(W(48, 'ai'), 'WITH AI', x=200, y=640, px=36, fam='M', align='left', alpha=0.7, sfx=None),
    bar(W(48, 'ai'), 200, 680, 1520, 70, 0.442, d=0.6, note=3),
    count(W(49, 'fifty'), 0, 56, y=940, px=200, d=0.8, suf='% FASTER'),
], chap=C3, src='Source: Peng et al., "The Impact of AI on Developer Productivity" (2023). 55.8% faster.')
scene(50, [
    txt(W(50), 'M.I.T. STUDY: PROFESSIONALS WRITING WITH CHATGPT', y=220, px=34, fam='M', alpha=0.7, sfx=None),
    txt(W(51, 'time'), 'TIME', x=560, y=420, px=60, fam='M', alpha=0.7, sfx=None),
    count(W(51, 'forty'), 0, 40, x=560, y=660, px=260, d=0.8, pre='-', suf='%'),
    txt(W(51, 'quality'), 'QUALITY', x=1360, y=420, px=60, fam='M', alpha=0.7, sfx=None),
    count(W(51, 'eighteen'), 0, 18, x=1360, y=660, px=260, d=0.8, pre='+', suf='%'),
], chap=C3, src='Source: Noy & Zhang, Science (2023).')
scene(52, [
    txt(W(52), 'BOSTON CONSULTING GROUP: CONSULTANTS + GPT-4', y=220, px=34, fam='M', alpha=0.7, sfx=None),
    count(W(53), 0, 25, x=560, y=620, px=260, d=0.8, suf='%'),
    txt(W(53, 'faster'), 'FASTER', x=560, y=740, px=60, fam='M', sfx=None),
    count(W(53, 'forty'), 0, 40, x=1360, y=620, px=260, d=0.8, suf='%'),
    txt(W(53, 'higher'), 'HIGHER QUALITY', x=1360, y=740, px=60, fam='M', sfx=None),
], chap=C3, src='Source: Dell\'Acqua et al., Harvard Business School working paper (2023).')
scene(54, [
    txt(W(54), 'CUSTOMER SUPPORT: AI ASSISTANT, 5,179 AGENTS', y=220, px=34, fam='M', alpha=0.7, sfx=None),
    txt(W(54, 'productivity'), 'EVERYONE', x=200, y=440, px=44, fam='M', align='left', sfx=None),
    bar(W(54, 'fourteen'), 200, 470, 1200, 90, 14 / 34, d=0.5, note=2),
    count(W(54, 'fourteen'), 0, 14, x=1720, y=550, px=110, d=0.5, pre='+', suf='%', align='right', sfx=None),
    txt(W(55), 'BEGINNERS', x=200, y=680, px=44, fam='M', align='left', sfx=None),
    bar(W(55, 'thirty'), 200, 710, 1200, 90, 1.0, d=0.7, note=5),
    count(W(55, 'thirty'), 0, 34, x=1720, y=790, px=110, d=0.7, pre='+', suf='%', align='right', sfx=None),
], chap=C3, src='Source: Brynjolfsson, Li & Raymond, "Generative AI at Work" (NBER, 2023).')
scene(56, [                                     # the one inverted scene
    txt(W(56, 'biggest'), 'THE BIGGEST GAINS WENT TO', y=340, px=90),
    txt(W(56, 'beginners'), 'BEGINNERS.', y=620, px=300, anim='slam', sfx='slam'),
    dict(k='gap', t=W(57, 'gap'), t2=W(57, 'expert'), y=800, sfx='gap'),
], chap=C3, inv=True)
scene(58, [
    txt(W(58), 'WHO STARTS COMPANIES NOW', y=220, px=34, fam='M', alpha=0.7, sfx=None),
    txt(W(59, 'single'), 'NEW STARTUPS WITH A SINGLE FOUNDER', y=300, px=60),
    rule(W(59), 460, 860, 1000),
    txt(W(59), '2019', x=760, y=920, px=40, fam='M', sfx=None),
    bar(W(59, 'twenty', 1), 640, 860, 240, 380, 23.7 / 36.3, d=0.7, note=1),
    count(W(59, 'twenty', 1), 0, 24, x=760, y=860 - 380 * 23.7 / 36.3 - 30, px=90, d=0.7, suf='%', sfx=None),
    txt(W(60, 'first'), 'H1 2025', x=1160, y=920, px=40, fam='M', sfx=None),
    bar(W(60, 'thirty'), 1040, 860, 240, 380, 1.0, d=0.8, note=4),
    count(W(60, 'thirty'), 0, 36, x=1160, y=860 - 380 - 30, px=90, d=0.8, suf='%', sfx=None),
], chap=C3, src='Source: Carta, Solo Founders Report 2025 (23.7% to 36.3%).')
scene(61, [
    txt(W(61), 'MORE PEOPLE ARE BUILDING ALONE.', y=460, px=130),
    txt(W(61, 'because'), 'BECAUSE NOW THEY CAN.', y=700, px=130, anim='slam', sfx='slam'),
], chap=C3)

# ---------------- 04 THE HONEST PART ----------------
scene(62, [
    txt(W(62), "NOW, LET'S BE HONEST.", y=440, px=150),
    txt(W(63), 'THIS IS NOT A GET-RICH-QUICK STORY.', y=660, px=80, sfx='hit'),
], chap=C4)
scene(64, [
    txt(W(64), 'RENT IS HIGH.', x=200, y=300, px=110, align='left', sfx='tick'),
    txt(W(64, 'groceries'), 'GROCERIES ARE HIGH.', x=200, y=440, px=110, align='left', sfx='tick'),
    txt(W(65), 'COMPETITION IS REAL.', x=200, y=580, px=110, align='left', sfx='tick'),
    txt(W(66), 'MANY NEW BUSINESSES STILL FAIL.', x=200, y=720, px=110, align='left', sfx='tick'),
    txt(W(67), 'EASIER DOES NOT MEAN GUARANTEED.', y=920, px=70, sfx='hit'),
], chap=C4)
scene(68, [
    txt(W(68), 'BUT NOTICE WHAT CHANGED.', y=240, px=46, fam='M', alpha=0.8, sfx='tick'),
    txt(W(69), 'THE OBSTACLE USED TO BE', y=420, px=60, fam='M', alpha=0.7, sfx=None),
    txt(W(69, 'permission'), 'PERMISSION + MONEY', y=560, px=130),
    strike(W(70), 400, 1520, 510),
    txt(W(70), 'NOW IT IS MOSTLY ONE THING:', y=720, px=46, fam='M', sfx=None),
    txt(W(70, 'starting'), 'STARTING.', y=920, px=200, anim='slam', sfx='slam'),
], chap=C4)
scene(71, [
    dict(k='gate', t=W(71, 'gone'), y=540, sfx='gate'),
    txt(W(71), 'THE GATE IS', y=500, px=140, sfx=None),
    txt(W(71, 'gone'), 'GONE.', y=720, px=240, anim='slam', sfx=None),
], chap=C4)
scene(72, [
    txt(W(72, 'loan'), 'NO LOAN', x=200, y=320, px=130, align='left', sfx='pluck0'),
    txt(W(72, 'test'), 'to test an idea.', x=1720, y=320, px=44, fam='M', align='right', sfx=None),
    txt(W(73, 'team'), 'NO TEAM', x=200, y=520, px=130, align='left', sfx='pluck2'),
    txt(W(73, 'first'), 'to build a first version.', x=1720, y=520, px=44, fam='M', align='right', sfx=None),
    txt(W(74, 'problem'), 'A PROBLEM WORTH SOLVING.', x=200, y=750, px=100, align='left', sfx='pluck4'),
    txt(W(74, 'weekend'), 'A WEEKEND.', x=200, y=880, px=100, align='left', sfx='hit'),
], chap=C4)
scene(75, [
    txt(W(75), 'PICK ONE SKILL.', y=300, px=130, sfx='hit'),
    txt(W(75, 'pick', 1), 'PICK ONE PROBLEM.', y=460, px=130, sfx='hit'),
    txt(W(76), 'PUT IT IN FRONT OF REAL PEOPLE.', y=660, px=90),
    txt(W(76, 'learn'), 'LEARN FAST.', y=870, px=180, anim='slam', sfx='slam'),
], chap=C4)
scene(77, [
    txt(W(77, 'headline'), 'NEXT TIME A HEADLINE SAYS "IMPOSSIBLE,"', y=300, px=80),
    txt(W(78), 'REMEMBER THE NUMBERS.', y=480, px=130, sfx='hit'),
    txt(W(79, 'cheaper'), 'CHEAPER.', x=440, y=780, px=130, sfx='pluck0'),
    txt(W(79, 'faster'), 'FASTER.', x=960, y=780, px=130, sfx='pluck2'),
    txt(W(79, 'smarter'), 'SMARTER.', x=1480, y=780, px=130, sfx='pluck4'),
], chap=C4)
scene(80, [
    txt(W(80), 'THE ONLY QUESTION LEFT:', y=360, px=60, fam='M', alpha=0.8, sfx='tick'),
    txt(W(81), 'WHAT ARE', y=560, px=170, sfx=None),
    txt(W(81, 'you'), 'YOU', y=860, px=300, anim='slam', sfx='slam'),
    txt(W(81, 'build'), 'GOING TO BUILD?', y=960, px=60, fam='M', sfx='tick'),
], chap=C4)

DUR = round(E(81) + 2.2, 2)
for i, s in enumerate(S):
    s['end'] = S[i + 1]['start'] if i + 1 < len(S) else DUR
wipes = sum(s['trans'] == 'wipe' for s in S)
assert wipes <= 3 and sum(s['inv'] for s in S) == 1
C = dict(vo_offset=OFF, dur=DUR, scenes=S,
         chapters=[[0, 'Intro'], [W(7) - 0.15, 'What it used to take'], [W(21) - 0.15, 'The record numbers'],
                   [W(33) - 0.15, 'The AI multiplier'], [W(62) - 0.15, 'The honest part']])
json.dump(C, open('cues.json', 'w'))
print(len(S), 'scenes, dur', DUR)
for c in C['chapters']:
    print(f"{int(c[0]//60)}:{int(c[0]%60):02d} {c[1]}")
lens = [s['end'] - s['start'] for s in S]
print('scene len min/max', round(min(lens), 2), round(max(lens), 2))
