#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


def main():
    for word in sys.argv[1:]:
        syllables = hyphenate(word)
        print '-'.join(syllables)


#
# Tavutussäännöt
# (Suoraan täältä pastettu:
#  http://www.cs.tut.fi/~laaja/lv98-99/harjoitustyo/tavutus.html)
#
# Suomen kielen tavuttaminen seuraa melko suoraviivaisesti seuraavia sääntöjä:
#
# 1. Konsonanttisääntö: Jos tavuun kuuluvaa vokaalia seuraa yksi tai useampia
#    konsonantteja, joita vielä seuraa vokaali, tavuraja sijoittuu välittömästi
#    ennen viimeistä konsonanttia.
# Esimerkkejä: lef-fas-sa ki-vaa kah-del-le: tra-giik-kaa se-kä hork-ka-ti-lo-ja
#
# 2. Vokaalisääntö: Jos tavun ensimmäistä vokaalia seuraa toinen vokaali, niiden
# väliin tulee tavuraja, ellei
# a) edellinen vokaali ole sama kuin jälkimmäinen (pitkä vokaali).
# b) jälkimmäinen vokaali ole i (i:hin loppuva diftongi).
# c) kysymyksessä ole jokin vokaalipareista
#    au, eu, ey, ie, iu, ou, uo, yö, äy tai öy (muu diftongi).
# Esimerkkejä: lu-en-to Aa-si-an kää-pi-ö-puo-lu-eis-ta
#
# 3. Diftongisääntö: Jos tavun kuuluvaa diftongia tai pitkää vokaalia seuraa
#    vokaali, tähän väliin tulee aina tavuraja.
# Esimerkkejä: raa-is-tu-nut maa-il-ma,
#              liu-ot-ti-met lau-an-tai-na tau-ot-ta leu-an al-la
#
# 4. Poikkeussääntö: Poikkeussanojen oikea tavutus on joko tiedettävä tai
#                    arvattava.
#    (Näitä ei oteta koodissa huomioon. Onnea matkaan.)
#
#


def hyphenate(word):
    """ Jakaa sanan word tavuihin.
    Palauttaa listan, jonka jokainen elementti on yksittäinen tavu merkkijonona
    """
    syllables = []  # final list of syllables in the word
    syl = []        # temp. syllable holder
    diphthongs = ('aa', 'ai', 'au', 'ee', 'ei', 'eu', 'ey', 'ie', 'ii', 'iu',
                  'oi', 'oo', 'ou', 'ui', 'uo', 'uu', 'yi', 'yy', 'yö', 'äi',
                  'äy', 'ää', 'öi', 'öy', 'öö')
    crule = False      # Konsonanttisääntö tulossa?
    has_vocal = False  # Tavun ensimmäinen vokaali löytynyt?
    diphthong = False  # Onko diftongisääntö katkaissut edellisen tavun?
    w = list(word.lower())

    for i, c in enumerate(w):
        if diphthong:
            diphthong = False
            continue

        if syl == []:
            has_vocal = False

        if crule and i < len(w)-1:
            if letter_type(c) == 'consonant' and letter_type(w[i+1]) == 'vowel':
                syllables.append(''.join(syl))
                syl = []
                crule = False

        syl.append(c)

        if i < len(w)-2:
            next = w[i+1]
            pair = ''.join([c, next])

            # diftongisääntö
            if pair in diphthongs and letter_type(w[i+2]) == 'vowel':
                # tavu katkee nyt (tai oikeestaan vasta kohdasta w[i+2].
                # Toteutuu heti seuraavan iteraation alussa)
                # Seuraava kirjain kuuluu vielä tähän tavuun
                syl.append(next)

                syllables.append(''.join(syl))
                syl = []
                diphthong = True
                continue

            # vokaalisääntö
            if letter_type(c) == 'vowel' and letter_type(next) == 'vowel':
                if not has_vocal:
                    has_vocal = True
                    if next != 'i' and pair not in diphthongs:
                        # tavu katkee nyt
                        syllables.append(''.join(syl))
                        syl = []
                        continue

            if has_consonant_break(w[i:]):
                crule = True

    # Viimeinen tavu uunista ulos ja tämä on ohi
    syllables.append(''.join(syl))
    return syllables


def has_consonant_break(s):
    """ Etsii merkkijonosta s katkaisevaa konsonanttisääntöä.
    Palauttaa True, jos sääntö löytyy, muutoin False.
    """
    if len(s) < 2:
        return False

    if letter_type(s[0]) != 'vowel':
        return False
    if letter_type(s[1]) != 'consonant':
        return False
    for i in range(1, len(s)):
        if letter_type(s[i]) == 'vowel':
            return True
    return False


def letter_type(c):
    if c.lower() in 'aeiouyäö':
        return 'vowel'
    else:
        return 'consonant'


if __name__ == "__main__":
    main()
