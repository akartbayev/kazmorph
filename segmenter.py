#-*- coding: utf-8 -*-
import itertools
import nltk
import sys, os

class ReadCorpus(object):
    def __init__(self):
        if len(sys.argv) < 2:
            sys.exit('Usage: %s file-name' % sys.argv[0])
        if not os.path.exists(sys.argv[1]):
            sys.exit('ERROR: File %s was not found!' % sys.argv[1])
        self.fileName = sys.argv[1]            
             
    def __iter__(self):
        for line in open(self.fileName):
            yield line.strip('\r\n')

def parse(lexem):
    suffix = ''
    word = lexem.decode('utf-8')
    poss = [u'ыңыз',u'іңіз',u'ымыз',u'iмiз',u'мыз',u'мiз',u'ңыз',u'ңiз',
            u'сы',u'сi',u'ым',u'iм',u'ың',u'ің']
    nums = [u'лар',u'лер',u'дар',u'дер',u'тар',u'тер']
    personals = [u'мын',u'мiн',u'бын',u'бiн',u'пын',u'пiн',u'мыз',u'мiз',u'быз',u'бiз',
                 u'пыз',u'пiз',u'сың',u'сiң',u'сыз',u'сiз']
    participle1s = [u'ған',u'ген',u'қан',u'кен',u'атын',u'етiн',u'йтын',u'йтiн',u'ушы',u'ушi']
    participle2s = [u'ғалы',u'гелi',u'қалы',u'келi',u'ып',u'iп']
    cases = [u'ның', u'нің', u'дың', u'дің', u'тың', u'тің', u'ға',u'ге', u'қа', u'ке', u'на', u'не',
              u'ды',u'ді', u'ты',u'ті', u'ны',u'ні',u'да',u'де',u'та',u'те',u'нда',u'нде',u'нан',u'нен',
              u'дан',u'ден', u'тан',u'тен',u'мен', u'бен', u'пен']
    advs = [u'дайын',u'дейін',u'тайын',u'тейін',u'шалық',u'шелік',u'шама',u'шеме',u'дай',
            u'дей',u'тай',u'тей',u'лай',u'лей',u'сын',u'сiн',u'ша',u'ше']
    pron = [u'сен',u'мен',u'сіз',u'ол',u'біз',u'олар',u'өз',u'бұл',u'мынау',u'осы',u'мына',
            u'анау',u'ана',u'сол',u'кім',u'не',u'неше',u'қанша',u'қайда',u'қайдан',u'қашан',
            u'қалай',u'қандай',u'қайсы',u'бәрі',u'барлық',u'бүкіл',u'барша',u'әр',u'әрбір',
            u'әркім',u'әрқайда',u'әрқашан',u'әрдайым',u'әрқалай',u'әрқайсысы',u'біреу',u'бірдеме',
            u'әлдеқандай',u'әлдеқайда',u'әлдеқашан',u'бірнеше',u'біраз',u'кей',u'кейбір',u'ештеме',
            u'ештеңе',u'дәнеме',u'ешнәрсе',u'ешкім',u'ешқандай',u'ешбiр',u'ешбiр',u'ешбiр',u'ешбiр',
            u'ешқашан',u'ешқайда',u'ешқалай',u'ешқайсысы']
    num = [u'бiр',u'екi',u'үш',u'төрт',u'бес',u'алты',u'жетi',u'сегiз',u'тоғыз',u'нөл',u'он',
           u'жиырма',u'отыз',u'қырық',u'елу',u'алпыс',u'жетпiс',u'сексен',u'тоқсан',u'жүз',u'мың']
    pstp = [u'үшiн',u'туралы',u'жайында',u'жөнiнде',u'бойынша',u'бойында',u'бойы',u'сайын',
            u'арқылы',u'сияқты',u'кейiн',u'соң',u'берi',u'басқа',u'бұрын',u'әрi',u'астам',
            u'гөрi',u'көрi',u'дейiн',u'шейiн',u'қарай',u'салым',u'жуық',u'таман',u'тарта',
            u'сәйкес',u'орай',u'бiрге',u'қатар',u'қабат']
    aux = [u'үстi',u'асты',u'алды',u'арты',u'iшi',u'сырты',u'ара',u'қарсы',u'қасы',u'жаны',u'маңы',
           u'түбi',u'орта',u'орталық',u'айнала',u'бетi',u'басы',u'аяғы',u'бойы']
    union = [u'және',u'әрi',u'да',u'де',u'та',u'те',u'бен',u'пен',u'мен',u'ал',u'бірақ',u'сонда',
             u'сөйтсе',u'әйтсе',u'алайда',u'дегенмен',u'онда',u'әйткенмен',u'әйтпегенде',u'әйтпесе',
             u'болмаса',u'яки',u'не',u'немесе',u'болмаса',u'әлде',u'біресе',u'бірде',u'кейде',u'яғни',
             u'өйткені',u'себебі',u'неге',u'десең',u'сондықтан',u'егер',u'онда']
    particles = [u'ғой',u'қой',u'ай',u'ау',u'ақ',u'ғана',u'қана',u'тек',u'ақ',u'мыс',u'мiс',u'ды',u'дi',
                 u'ба',u'бе',u'па',u'пе',u'ма',u'ме',u'ше',u'түгiл']
    
    with open('/Users/Apple/Documents/workspace/corpora/ENKZdict/adj.kk') as f:
        adj = f.read().splitlines()
    with open('/Users/Apple/Documents/workspace/corpora/ENKZdict/adv.kk') as f:
        adv = f.read().splitlines()
    suflist = itertools.chain(poss, personals, participle1s, participle2s, advs,nums,cases)
    suffixes = sorted(suflist)
    exepts = itertools.chain(pstp, aux, pron, num, union, particles, adj, adv)
    if word not in exepts:
        found = True
        while found:
            found = False
            for s in suffixes:
                if word.endswith(s):
                    suffix = '[' + s + ']' + suffix
                    word = word[:-len(s)] # remove suffix from word
                    found = True
    else:
        suffix = 'none'

    return (lexem, word, suffix)

readCorpus = ReadCorpus() # doesn't load the corpus into memory!
suf = '.done'
f = open(sys.argv[1]+suf, 'w')
for line in readCorpus:
    tokens = nltk.word_tokenize(line)
    for token in tokens:
            f.write(parse(token)[1].encode('utf-8') + ' ' + parse(token)[2].encode('utf-8')+' ')
f.close()
