"""TEST DATA ONLY: a GabellaTalents dump of the paladin, ruRU + enUS, as the addon would write it. The layout is the 1.12 tree
from memory plus the Forever talents of our tables in free cells: it checks the engine, it is not a fact and never goes to
content/talents (tests/test_talents.py refuses fixture files there). Run: python tests/fixtures/talents/make_fixture.py"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
NAMES = json.load(open(os.path.join(ROOT, 'i18n', 'names.json'), encoding='utf-8'))
# name, row, col, ranks, prerequisite (row, col) or None, icon name (only for the fixture sprite)
TREES = [
    [('Divine Strength', 1, 2, 5, None, 'ability_golemthunderclap'), ('Divine Intellect', 1, 3, 5, None, 'spell_nature_sleep'),
     ('Reverence', 2, 1, 3, None, None), ('Spiritual Focus', 2, 2, 5, None, 'spell_arcane_blink'),
     ('Improved Seal of Righteousness', 2, 3, 5, None, 'ability_thunderbolt'),
     ('Healing Light', 2, 4, 3, None, 'spell_holy_holybolt'), ('Consecration', 4, 2, 1, None, 'spell_holy_innerfire'),
     ('Improved Lay on Hands', 3, 3, 2, None, 'spell_holy_layonhands'), ('Unyielding Faith', 3, 4, 2, None, 'spell_holy_unyieldingfaith'),
     ('Illumination', 3, 2, 5, None, 'spell_holy_greaterheal'), ('Improved Blessing of Wisdom', 4, 3, 2, None, 'spell_holy_sealofwisdom'),
     ('Divine Favor', 5, 2, 1, (4, 2), 'spell_holy_heal'), ('Lasting Judgement', 5, 3, 3, None, 'spell_holy_healingaura'),
     ('Voice of Truth', 4, 1, 1, None, None), ('Holy Power', 6, 3, 5, None, 'spell_holy_power'),
     ('Holy Shock', 4, 4, 1, None, 'spell_holy_searinglight')],
    [('Improved Devotion Aura', 1, 2, 5, None, 'spell_holy_devotionaura'), ('Redoubt', 1, 3, 5, None, 'ability_defend'),
     ('Precision', 2, 1, 3, None, 'ability_rogue_ambush'), ('Guardian\'s Favor', 2, 2, 2, None, 'spell_holy_sealofprotection'),
     ('Improved Seal of Fury', 2, 3, 1, None, None), ('Toughness', 2, 4, 5, None, 'spell_holy_devotion'),
     ('Blessing of Kings', 3, 1, 1, None, 'spell_magic_magearmor'), ('Improved Righteous Fury', 3, 2, 3, None, 'spell_holy_sealoffury'),
     ('Shield Specialization', 3, 3, 3, (1, 3), 'inv_shield_06'), ('Anticipation', 3, 4, 5, None, 'spell_magic_lesserinvisibilty'),
     ('Improved Hammer of Justice', 4, 2, 3, None, 'spell_holy_sealofmight'), ('Improved Concentration Aura', 4, 3, 3, None, 'spell_holy_mindsooth'),
     ('Blessing of Sanctuary', 5, 2, 1, None, 'spell_nature_lightningshield'), ('Reckoning', 5, 3, 5, None, 'spell_holy_blessingofstrength'),
     ('One-Handed Weapon Specialization', 6, 3, 5, None, 'inv_sword_20'), ('Templar\'s Bulwark', 6, 1, 1, None, None),
     ('Holy Shield', 7, 2, 1, (5, 2), 'spell_holy_blessingofprotection')],
    [('Improved Blessing of Might', 1, 2, 5, None, 'spell_holy_fistofjustice'), ('Benediction', 1, 3, 5, None, 'spell_frost_windwalkon'),
     ('Improved Judgement', 2, 1, 2, None, 'spell_holy_righteousfury'), ('Improved Seal of the Crusader', 2, 2, 3, None, 'spell_holy_holysmite'),
     ('Deflection', 2, 3, 5, None, 'ability_parry'), ('Holy Conduit', 2, 4, 2, None, None),
     ('Vindication', 3, 1, 3, None, 'spell_holy_vindication'), ('Conviction', 3, 2, 5, None, 'spell_holy_retributionaura'),
     ('Seal of Command', 3, 3, 1, None, 'ability_warrior_innerrage'), ('Pursuit of Justice', 3, 4, 2, None, 'spell_holy_persuitofjustice'),
     ('Eye for an Eye', 4, 1, 2, (3, 1), 'spell_holy_eyeforaneye'), ('Sanctified Judgement', 4, 2, 3, None, None),
     ('Improved Retribution Aura', 4, 3, 2, None, 'spell_holy_auraoflight'),
     ('Two-Handed Weapon Specialization', 5, 1, 3, None, 'inv_hammer_04'), ('Sanctity Aura', 5, 3, 1, None, 'spell_holy_mindvision'),
     ('Sacred Arbiter', 5, 4, 1, None, None), ('Vengeance', 6, 2, 5, (3, 2), 'ability_racial_avatar'),
     ('Repentance', 7, 2, 1, None, 'spell_holy_prayerofhealing')],
]
TABS = [('Holy', 'Свет'), ('Protection', 'Защита'), ('Retribution', 'Воздаяние')]


def lua(v, ind=1):
    pad = '\t' * ind
    if isinstance(v, dict):
        return '{\n' + ''.join(f'{pad}["{k}"] = {lua(x, ind + 1)},\n' for k, x in v.items() if x is not None) + '\t' * (ind - 1) + '}'
    if isinstance(v, list):
        return '{\n' + ''.join(f'{pad}{lua(x, ind + 1)}, -- [{i}]\n' for i, x in enumerate(v, 1)) + '\t' * (ind - 1) + '}'
    if isinstance(v, str):
        return '"' + v.replace(chr(92), chr(92) * 2).replace('"', chr(92) + '"') + '"'
    return str(v).lower() if isinstance(v, bool) else str(v)


def dump(locale):
    ru = locale == 'ruRU'
    trees = []
    for (en, rn), talents in zip(TABS, TREES):
        ts = []
        for i, (n, r, c, m, req, _) in enumerate(talents, 1):
            name = NAMES.get(n, {}).get('ru', n) if ru else n
            ts.append({'name': name, 'icon': 130000 + i, 'row': r, 'col': c, 'maxRank': m, 'talentID': 1000 + i,
                       'req': list(req) if req else None, 'tip': [name, ('Ранг 0/' if ru else 'Rank 0/') + str(m), 'TEST: ' + n]})
        trees.append({'info': [en, rn if ru else en], 'talents': ts})
    return {'class': 'PALADIN', 'locale': locale, 'build': '1.60.1.70532', 'interface': 11507, 'trees': trees}


if __name__ == '__main__':
    db = {'PALADIN': {'ruRU': dump('ruRU'), 'enUS': dump('enUS')}}
    open(os.path.join(HERE, 'GabellaTalents.lua'), 'w', encoding='utf-8', newline='\n').write('\nGabellaTalentsDB = ' + lua(db) + '\n')
    icons = {f'{k}-{i}': t[5] for k, ts in zip(('holy', 'protection', 'retribution'), TREES) for i, t in enumerate(ts, 1)}
    json.dump(icons, open(os.path.join(HERE, 'icons.json'), 'w', encoding='utf-8', newline='\n'), indent=1)
