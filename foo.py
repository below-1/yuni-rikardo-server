import json
import random
import pandas as pd

SLOT_TEMPLATE = [
  [3, 2, 2],
  [3, 2, 3],
  [3, 3, 2],
  [2, 3, 2],
  [3, 2],
  [2, 3]
]
BOBOT_HARI = [ 7, 8, 8, 7, 5, 5 ]

def load_json(p):
    with open(p) as f:
        data = json.load(f)
        return data


def _split_mpgs (mp_guru_list):
    tmp_mp_guru = []
    mp_guru_id = 1
    for mp_guru in mp_guru_list:
        if mp_guru["jam"] <= 3:

            mp_guru["id"] = mp_guru_id
            mp_guru_id += 1

            tmp_mp_guru.append(mp_guru)
        elif mp_guru["jam"] == 4:
            new_mp_guru = { **mp_guru }

            new_mp_guru["id"] = mp_guru_id
            mp_guru_id += 1

            new_mp_guru["jam"] = 2

            mp_guru["jam"] = 2

            mp_guru["id"] = mp_guru_id
            mp_guru_id += 1

            tmp_mp_guru.append(new_mp_guru)
            tmp_mp_guru.append(mp_guru)
        else:
            new_mp_guru = {**mp_guru }
            new_mp_guru["jam"] = mp_guru["jam"] - 3

            new_mp_guru["id"] = mp_guru_id
            mp_guru_id += 1

            mp_guru["jam"] = 3
            mp_guru["id"] = mp_guru_id
            mp_guru_id += 1

            tmp_mp_guru.append(new_mp_guru)
            tmp_mp_guru.append(mp_guru)
    return tmp_mp_guru

def load_mp_guru(p):
    data = load_json(p)
    data = _split_mpgs(data)
    return data
    # xs = pd.DataFrame(data)
    # return xs

def gen_pools(mpg, n_kelas, mp_target):
    def total_hours(li):
        return sum( x['jam'] for x in li )

    mps = set(mp_target.keys())
    pools = []
    for kelas in range(n_kelas):
        kelas_pools = []
        for mp in mps:
            n_choose = 1
            while True:
                sub_pools = [ m for m in mpg if m['mp_id'] == mp ]
                subs = random.sample(sub_pools, n_choose)
                n_choose = 1 if n_choose == 2 else 2
                nhours = total_hours(subs)
                if total_hours(subs) == mp_target[mp]:
                    kelas_pools.extend(subs)
                    break
        pools.append(kelas_pools)
    return pools

def gen_init(pools, mpg, n_kelas, mp_target):
    def filter_mpg(mpg_list, mp, guru, length):
        return [ (i, mpg) for (i, mpg) in enumerate(mpg_list)
            if (mpg['guru_id'] not in guru) and \
                (mpg['mp_id'] not in mp) and \
                (mpg['jam'] == length)
        ]

    def find_exist_mp_in_kelas(li, kelas, hari):
        li_kelas = [ x for x in li if x['kelas'] == kelas and x['hari'] == hari ]
        return { x['mp_id'] for x in li_kelas }

    def find_exist_guru_in_kelas(li, kelas, hari):
        li_kelas = [ x for x in li if x['kelas'] == kelas and x['hari'] == hari ]
        return { x['guru_id'] for x in li_kelas }

    def find_exist_guru_in_slot(li, hari, i):
        li_kelas = [ x for x in li if x['i'] == i and x['hari'] == hari ]
        return { x['guru_id'] for x in li_kelas }    

    result = []
    index = 0
    citer = 0
    for day in range(6):
        slots = SLOT_TEMPLATE[day]
        for i, slot_length in enumerate(slots):
            for kelas in range(n_kelas):
                sub_pools = [ (j, m) for j, m in enumerate(pools[kelas]) if m['jam'] == slot_length ]
                if len(sub_pools) == 0:
                    print(f'{sub_pools=}')
                si, selected = random.choice(sub_pools)
                result.append({
                    'guru_id': selected['guru_id'],
                    'mp_id': selected['mp_id'],
                    'jam': selected['jam'],
                    'guru_nama': selected['guru_nama'],
                    'mp_nama': selected['mp_nama'],
                    'i': i,
                    'kelas': kelas,
                    'hari': day
                })
                del pools[kelas][si]
                citer += 1
    return result

def calc_soft_violations(xs, morning_mp):
    violations = xs[ ( xs.mp_id.isin(morning_mp) ) & (xs.i != 0) ]
    return violations.shape[0], violations.index

def calc_sc1_violations(xs):
    total = 0
    index = set()
    for (kelas, hari), g in xs.groupby(['kelas', 'hari']):
        g_dups = g.duplicated('guru_id')
        mp_dups = g.duplicated('mp_id')
        total_g_dups = g_dups.sum()
        total_mp_dups = mp_dups.sum()
        if total_mp_dups > 0 or total_g_dups > 0:
            index = index.union(set(xs[(xs.kelas == kelas) & (xs.hari == hari)].index))
            total += 1
    return total, list(index)

def calc_hard_violations(xs):
    total = 0
    index = set()
    for _, g in xs.groupby(['hari', 'i']):
        dups = g.duplicated('guru_id')
        total += dups.sum()
        index = index.union(set( g[dups].index ))
    return total, list(index)

def check_total_mp_hours(xs, mp_target):
    for (kelas, mp_id), g in xs.groupby(['kelas', 'mp_id']):
        if g.sum().jam != mp_target[mp_id]:
            print(f'{kelas=}')
            print(f'{mp_id=}')
            print(f'{g.sum().mp_id}')
            raise Exception('total hours violated')

def swap_place(xs, a, b):
    xa = xs.iloc[a].copy()
    xb = xs.iloc[b].copy()
    if xa.jam != xb.jam:
        print(xa)
        print(xb)
        raise Exception(f'jam is not equal {xa.jam} != {xb.jam}')
    xs.at[a, 'mp_id'] = xb.mp_id
    xs.at[a, 'mp_nama'] = xb.mp_nama
    xs.at[a, 'guru_id'] = xb.guru_id
    xs.at[a, 'guru_nama'] = xb.guru_id
    xs.at[b, 'mp_id'] = xa.mp_id
    xs.at[b, 'mp_nama'] = xa.mp_id
    xs.at[b, 'guru_id'] = xa.guru_id
    xs.at[b, 'guru_nama'] = xa.guru_nama

def swap_time_in_kelas(xs, a, b):
    xa = xs.loc[a].copy()
    xb = xs.loc[b].copy()
    if xa.kelas != xb.kelas:
        raise Exception('not in same kelas')
    xs.at[a, 'hari'] = xb.hari
    xs.at[a, 'i'] = xb.i
    xs.at[b, 'hari'] = xa.hari
    xs.at[b, 'i'] = xa.i

def _main(mp_target, mpg, n_kelas):
    mp_guru_pools = {}
    for m in mpg:
        if m['mp_id'] not in mp_guru_pools:
            mp_guru_pools[m['mp_id']] = set()
        mp_guru_pools[m['mp_id']].add(m['guru_id'])

    pools = gen_pools(mpg, n_kelas, mp_target)
    initial = gen_init(pools, mpg, n_kelas, mp_target)
    xs = pd.DataFrame(initial)
    count = 0
    while count < 500:
        vio, vio_index = calc_hard_violations(xs)
        print(f'{vio=}')
        # input()
        if vio == 0:
            break
        # a = random.choice(xs.index)
        a = random.choice(vio_index)
        b = random.choice(xs[(xs.jam == xs.loc[a].jam) & (xs.kelas == xs.loc[a].kelas)].index)

        prob = random.random()
        mut = None
        prev_guru_id = None
        if prob > 0.5:
            swap_time_in_kelas(xs, a, b)
            mut = 'TIME'
        else:
            xa = xs.loc[a]
            guru_pools = mp_guru_pools[xa.mp_id]
            if len(guru_pools) > 1:
                mut = 'GURU'
                guru_id = random.choice(list(guru_pools))
                prev_guru_id = xa.guru_id
                xs.at[a, 'guru_id'] = guru_id

        new_vio, vio_index = calc_hard_violations(xs)
        if new_vio > vio:
            if mut == 'TIME':
                swap_time_in_kelas(xs, b, a)
            elif mut == 'GURU':
                xs.at[a, 'guru_id'] = prev_guru_id

        count += 1
    
    count = 0
    while count < 1000:
        count += 1
        sc_vio, sc_vio_index = calc_sc1_violations(xs)
        print(f'{sc_vio=}')
        # input()
        if sc_vio == 0:
            break
        a = random.choice(sc_vio_index)
        b = random.choice(xs[(xs.jam == xs.loc[a].jam) & (xs.kelas == xs.loc[a].kelas)].index)
        swap_time_in_kelas(xs, a, b)

        hc_vio, _ = calc_hard_violations(xs)
        if hc_vio > 0:
            swap_time_in_kelas(xs, b, a)
            continue

        sc_new_vio, _ = calc_sc1_violations(xs)
        if sc_new_vio > sc_vio:
            swap_time_in_kelas(xs, b, a)

    return xs

def f(mp_target, mpg, n_kelas):
    mpg_list = _split_mpgs(mpg)
    return _main(mp_target, mpg_list, n_kelas)

def decode(xs):
    result = []
    for (hari, i), group in xs.groupby(['hari', 'i']):
        sorted_g = group.sort_values(['kelas'])
        rows = []
        record = {
            'hari': int(hari),
            'i': int(i)
        }
        for i, row in sorted_g.iterrows():
            rows.append({
                'kelas': row.kelas,
                'guru_id': row.guru_id,
                'mp_id': row.mp_id,
                'jam': row.jam
            })
        print(rows[0])
        record['rows'] = rows
        record['jam'] = rows[0]['jam']
        result.append(record)
    return result

if __name__ == '__main__':
    mp_target = {
        1: 3,
        2: 6,
        3: 3,
        4: 5,
        5: 4,
        6: 4,
        7: 5,
        8: 3,
        9: 2,
        10: 3,
        11: 2
    }
    # morning_mp = [4, 6, 7]
    n_kelas = 11
    mpg = load_json('webapp/mp_guru.json')
    xs = f(mp_target, mpg, n_kelas)
    result = decode(xs)
    json.dumps(result)