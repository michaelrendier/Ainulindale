#!/usr/bin/env python3
"""Generate Ainulindale/AgeThird/D-CS_Memory.md from template.md.

Every listing is extracted from its source file, run cold in an empty temporary directory
(`python3 -I`), and its printed output is written into the paper. Transcripts are excerpts of
recorded benchmark outputs. `--check` rebuilds in memory and compares with the committed file.

    python3 make_paper.py            # write ../D-CS_Memory.md
    python3 make_paper.py --check    # exit 1 if the committed paper differs from the code
"""
import ast, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))          # .../ThePlace
HW = os.path.join(ROOT, 'PtolemyDesktop/Callimachus/HyperWebster-Data-Storage/hyperwebster.py')
WB = os.path.join(ROOT, 'VAPMIP/wordnet_boxkite.py')
MONAD = os.path.join(ROOT, 'VAPMIP/monad.py')
SCRATCH = os.path.join(ROOT, 'ContextPlease/claude/scratchpad/2026-09-29_hyperwebster_overhead')
OUT = os.path.join(HERE, '..', 'D-CS_Memory.md')


def lines_of(path, node):
    return open(path).read().split('\n')[node.lineno - 1:node.end_lineno]


def hyperwebster_core(chars_expr):
    tree = ast.parse(open(HW).read())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'HyperWebster')
    chars = next(n for n in cls.body if isinstance(n, ast.Assign) and n.targets[0].id == '_DEFAULT_CHARS')
    meths = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in ('point_to_text', 'regenerate_text')]
    body = ['class HyperWebster:'] if chars_expr is None else ['class HyperWebster:']
    if chars_expr is None:
        body += lines_of(HW, chars)
        body += ['', '    def __init__(self, characters=_DEFAULT_CHARS):          # class shell (added); the shipped __init__ also sets the int limit']
    else:
        body += ['    def __init__(self, characters=%r):                      # class shell (added)' % chars_expr]
    body += ['        self.characters = characters; self.char_list = list(characters); self.N = len(self.char_list)',
             '        self._char_index = {ch: i for i, ch in enumerate(self.char_list)}', '']
    for m in meths:
        body += lines_of(HW, m) + ['']
    return '\n'.join(body).rstrip('\n') + '\n'


L1 = hyperwebster_core(None) + '''
hw = HyperWebster(); text = "Hello, World!"
a = hw.point_to_text(text)
print('N =', hw.N, '; address of', repr(text), '=', a)
print('round trip exact:', hw.regenerate_text(a) == text, '; address bits:', a.bit_length(), 'for', len(text), 'characters')
'''
L2 = hyperwebster_core('ab') + '''
import itertools
rows = []
for L in (1, 2, 3):
    for t in itertools.product('ab', repeat=L):
        s = ''.join(t); rows.append((HyperWebster().point_to_text(s), s))
rows.sort()
print('  '.join('%d:%s' % (a, s) for a, s in rows))
print('addresses are exactly 0..%d with no gap and no repeat:' % (len(rows) - 1), [a for a, _ in rows] == list(range(len(rows))))
print('every address regenerates its string:', all(HyperWebster().regenerate_text(a) == s for a, s in rows))
'''
L3 = '''import math
N = 97
print('bits per character at N = 97: %.3f ; against 8 bits per byte: %.3f of raw' % (math.log2(N), math.log2(N) / 8))
print('97^38 <= 2^256:', N ** 38 <= 2 ** 256, '; 97^39 <= 2^256:', N ** 39 <= 2 ** 256, '=> a 256-bit address holds at most 38 characters')
print('bits needed for 38 characters:', (N ** 38 - 1).bit_length(), 'against 38 x 8 = 304 raw bits (%.3f)' % ((N ** 38 - 1).bit_length() / 304))
print('bits needed for 32 characters:', (N ** 32 - 1).bit_length(), 'but a fixed 256-bit field costs 256 against 32 x 8 = 256 raw (ratio 1.000)')
'''


def wordnet_core():
    src = open(WB).read(); tree = ast.parse(src)
    pick = []
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name in ('_sieve', 'spelling_code'): pick.append(n)
        if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') in ('_P', 'LETTER_CAP'): pick.append(n)
        if isinstance(n, ast.AnnAssign) and getattr(n.target, 'id', '') == 'LETTER_PRIMES': pick.append(n)
    out = ['from typing import List', '']
    for n in sorted(pick, key=lambda x: x.lineno):
        out += lines_of(WB, n) + ['']
    return '\n'.join(out)


L4 = wordnet_core() + '''
def decode(code, nletters):                      # factor the code at the position primes (for words of 20 letters or fewer)
    out = ''
    for i in range(nletters):
        p, e = LETTER_PRIMES[i], 0
        while code % p == 0: code //= p; e += 1
        out += chr(ord('a') + e - 1)
    return out

naive = lambda w: __import__('math').prod({c: p for c, p in zip('abcdefghijklmnopqrstuvwxyz', _P)}[c] for c in w)
print('naive prime-per-letter product : cat', naive('cat'), '= act', naive('act'), '; listen', naive('listen'), '= silent', naive('silent'))
print('spelling_code                   : cat == act:', spelling_code('cat') == spelling_code('act'), '; listen == silent:', spelling_code('listen') == spelling_code('silent'))
print('spelling_code("cat") =', spelling_code('cat'))
print('decoded:', [decode(spelling_code(w), len(w)) for w in ('cat', 'act', 'windspeed', 'reconstructible')])
a, b = 'a' + 'x' * 19 + 'c', 'b' + 'x' * 19 + 'b'
print('two different 21-letter words, same code (positions 0 and 20 share the base 2, 1+3 = 2+2):', spelling_code(a) == spelling_code(b))
import random
words = [w.strip().lower() for w in open('/usr/share/dict/words') if w.strip().isalpha()]
random.seed(0); sample = random.sample(sorted(set(words)), 30000)
short = [w for w in sample if len(w) <= 20]; long_ = [w for w in sample if len(w) > 20]
ok = sum(decode(spelling_code(w), len(w)) == w for w in short)
print('sample of 30,000 dictionary words: %d have <= 20 letters, exact recovery %d (%.3f %%); %d have more than 20 letters' % (len(short), ok, 100 * ok / len(short), len(long_)))
'''


def monad_core():
    lines = open(MONAD).read().split('\n')[140:207]            # lines 141-207
    return 'from typing import List\n\n' + '\n'.join(lines).rstrip('\n') + '\n'


L5 = monad_core() + '''
import collections, random
words = sorted({w.strip().lower() for w in open('/usr/share/dict/words') if w.strip().isalpha()})
random.seed(0); sample = random.sample(words, 5000)
idx = collections.Counter(_word_zero_idx(w) for w in sample)
print('5,000 dictionary words -> %d distinct indices (limit 6,542); largest share of one index: %d words' % (len(idx), max(idx.values())))
print('listen -> %d ; silent -> %d ; piano -> %d ; melancholy -> %d' % tuple(_word_zero_idx(w) for w in ('listen', 'silent', 'piano', 'melancholy')))
print('words sharing an index with another word in the sample: %d of 5,000' % sum(c for c in idx.values() if c > 1))
'''


def run(code):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'listing.py'); open(p, 'w').write(code)
        r = subprocess.run([sys.executable, '-I', p], capture_output=True, text=True, cwd=d, timeout=280)
    if r.returncode: raise SystemExit('listing failed:\n' + r.stderr[-800:])
    return r.stdout.rstrip('\n')


def excerpt(fname, start_pat, nlines):
    L = open(os.path.join(SCRATCH, fname)).read().split('\n')
    i = next(k for k, l in enumerate(L) if start_pat in l)
    return '\n'.join(l.rstrip() for l in L[i:i + nlines])


def build():
    t = open(os.path.join(HERE, 'template.md')).read()
    listings = {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4, 'L5': L5}
    for k, code in listings.items():
        t = t.replace('{{%s}}' % k, code.rstrip('\n')).replace('{{O%s}}' % k[1], run(code))
    t = t.replace('{{T1}}', excerpt('bench_output_2026-11-14.txt', 'english_corpus.txt (prose)', 13))
    t = t.replace('{{T2}}', excerpt('bench_layers2_output_2026-11-14.txt', 'corpus 4000 chars', 7))
    t = t.replace('{{ABSTRACT}}', open(os.path.join(HERE, 'abstract.md')).read().rstrip('\n'))
    assert '{{' not in t, 'unreplaced placeholder'
    return t


if __name__ == '__main__':
    text = build()
    if '--check' in sys.argv:
        same = os.path.exists(OUT) and open(OUT).read() == text
        print('paper matches the code' if same else 'PAPER DIFFERS FROM THE CODE'); sys.exit(0 if same else 1)
    open(OUT, 'w').write(text); print('wrote', os.path.abspath(OUT), len(text.split()), 'words')
