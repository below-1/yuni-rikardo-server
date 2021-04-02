import random
import numpy as np
import numpy.ma as ma
import time
import json
import pandas as pd
from itertools import combinations

from collections import namedtuple

PoolItem = namedtuple('PoolItem', ['mp_id', 'jam', 'mpg', 'id'])
SlotItem = namedtuple('SlotItem', ["item", "h", "t0", "t1"])

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


class KelasSolutionGenerator:

    def __init__(self, **kwargs):
        self.exists = set()
        self.bobot_hari = kwargs['bobot_hari']
        self.mp_guru_list = kwargs['mp_guru_list']
        self.mp_list = kwargs['mp_list']
        self.kelas_list = kwargs['kelas_list']

    def _total_hours(self, X):
        return sum(it.jam for it in X)

    def _gen_mp_guru_pools(self):
        result = []
        total_all_hours = self._total_hours(result)
        for mp in self.mp_list:
            mp_id = mp['id']
            target_jam = mp['jpm']
            mpg_pool = [ mpg for mpg in self.mp_guru_list if mpg['mp_id'] == mp_id ]
            n_mpg = 1
            selected_mpg = random.sample(mpg_pool, n_mpg)
            total_mp_hours = sum(mpg['jam'] for mpg in selected_mpg)
            while total_mp_hours != target_jam:
                n_mpg = random.randint(1, len(mpg_pool))
                selected_mpg = random.sample(mpg_pool, n_mpg)
                total_mp_hours = sum(mpg['jam'] for mpg in selected_mpg)
            for mpg in selected_mpg:
                jam = mpg['jam']
                pool_item = PoolItem(mp_id, jam, mpg, mpg['id'])
                result.append(pool_item)
        return result

    def _gen(self):
        pools = self._gen_mp_guru_pools()
        mp_hours = {}
        current_mp_hours = {}
        for mp in self.mp_list:
            mp_id = mp['id']
            if mp_id not in mp_hours:
                mp_hours[mp_id] = 0
            mp_hours[mp_id] += mp['jpm']
            current_mp_hours[mp_id] = 0

        result = []
        for day in range(6):
            day_data = self.bobot_hari[day]
            max_bobot = day_data["max"]
            citer = 0
            max_iter = 100
            while True:
                citer += 1
                if citer > max_iter:
                    raise Exception('max_iter')

                uniq_mp_ids = list(set(it.mp_id for it in pools))
                n_mp = random.randint(2, 4)
                if n_mp > len(uniq_mp_ids):
                    n_mp = len(uniq_mp_ids)
                sample_mp_ids = set(random.sample(uniq_mp_ids, n_mp))
                filtered_pools = [ it for it in pools if it.mp_id in sample_mp_ids ]
                day_result = []
                for mp_id in sample_mp_ids:
                    filtered_by_mp_id = [ it for it in filtered_pools if it.mp_id == mp_id ]
                    mpg = random.choice(filtered_by_mp_id)
                    day_result.append(mpg)
                current_day_hours = sum( it.jam for it in day_result )
                if current_day_hours != max_bobot:
                    continue
                total_mp_hours_violated = False
                for item in day_result:
                    next_mp_total_hours = current_mp_hours[item.mp_id] + item.jam
                    if next_mp_total_hours > mp_hours[item.mp_id]:
                        total_mp_hours_violated = True
                        break
                if total_mp_hours_violated:
                    continue
                curr_t = 0
                for item in day_result:
                    current_mp_hours[item.mp_id] += item.jam
                    if current_mp_hours[item.mp_id] == mp_hours[item.mp_id]:
                        pools = [ it for it in pools if item.mp_id != it.mp_id ]
                    t0 = curr_t
                    t1 = t0 + item.mpg['jam'] - 1
                    curr_t = t1 + 1
                    slot_item = SlotItem(
                        item=item, 
                        h=day, 
                        t0=t0, 
                        t1=t1
                    )
                    result.append(slot_item)
                break
        return result

    def generate(self):
        while True:
            try:
                result = self._gen()
                return result
            except Exception:
                print('restarting')
                continue


def generate_initial_solution(data):
    result = []
    for kelas in data['kelas_list']:
        generator = KelasSolutionGenerator(**data)
        kelas_result = generator.generate()
        for slot in kelas_result:
            result.append([
                kelas['id'], 
                slot.item.mpg['guru_id'], 
                slot.item.mpg['mp_id'], 
                slot.h,
                slot.t0, 
                slot.t1,
                slot.t1 - slot.t0 + 1
            ])
    return pd.DataFrame(result, columns=["kelas", "guru", "mp", "hari", "t0", "t1", 'jam'])

def spread_solutions(data):
    mpg_array = []
    guru_array = []
    for kelas in data:
        mpg_kelas = []
        guru_kelas = []
        for day in kelas:
            for item in day:
                for i in range(item.jam):
                    mpg_kelas.append(item.id)
                    guru_kelas.append(item.mpg['guru_id'])
        mpg_array.append(mpg_kelas)
        guru_array.append(guru_kelas)
    return {
        "mpg": np.array(mpg_array),
        "guru": np.array(guru_array)
    }

def calc_violations(xs):
    violations = 0
    all_dups = []
    for _, group in xs.groupby(['hari', 't0', 't1']):
        dups = group.duplicated('guru')
        dups_ind = dups[dups == True].index
        all_dups.extend(dups_ind.to_list())
        violations += len(dups_ind)
    return violations, all_dups

def find_ind_pools(xs, jam):
    ind_pools = xs[xs['jam'] == jam].index.to_list()

def swap_time(xs, a, b):
    _hari = xs.loc[a].hari
    _t0 = xs.loc[a].t0
    _t1 = xs.loc[a].t1
    xs.loc[a, 'hari'] = xs.loc[b].hari
    xs.loc[a, 't0'] = xs.loc[b].t0
    xs.loc[a, 't1'] = xs.loc[b].t1
    xs.loc[b, 'hari'] = _hari
    xs.loc[b, 't0'] = _t0
    xs.loc[b, 't1'] = _t1

def swap_kelas(xs, a, b):
    temp = xs.loc[a].copy()

    xs.loc[a, 'kelas'] = xs.loc[b].kelas
    xs.loc[a, 'hari'] = xs.loc[b].hari
    xs.loc[a, 't0'] = xs.loc[b].t0
    xs.loc[a, 't1'] = xs.loc[b].t1

    xs.loc[b, 'kelas'] = temp.kelas
    xs.loc[b, 'hari'] = temp.hari
    xs.loc[b, 't0'] = temp.t0
    xs.loc[b, 't1'] = temp.t1

def choose_same_jam(xs, a):
    jam = xs.loc[a].jam
    return xs.index[xs['jam'] == jam]

def mutate_01(xs, a):
    tgt_kelas = xs.loc[a].kelas
    tgt_jam = xs.loc[a].jam
    tgt_mp = xs.loc[a].mp
    selectors = (xs['kelas'] == tgt_kelas) & (xs['jam'] == tgt_jam)
    ind_pools = xs[selectors].index.difference([a]).to_list()
    b = random.choice(ind_pools)
    swap_time(xs, a, b)
    return b

def mutate_02(xs, a):
    tgt_kelas = xs.loc[a].kelas
    tgt_jam = xs.loc[a].jam
    tgt_mp = xs.loc[a].mp
    selectors = (xs['kelas'] != tgt_kelas) & \
        (xs['mp'] == tgt_mp) & \
        (xs['jam'] == tgt_jam)
    ind_pools = xs[selectors].index.difference([a]).to_list()
    b = random.choice(ind_pools)
    swap_kelas(xs, a, b)
    return b

def mutate(xs, a):
    # x = random.random()
    # return mutate_01(xs, a) if x > 0.5 else mutate_02(xs, a)
    return mutate_01(xs, a)

def _main(data):
    data['mp_guru_list'] = _split_mpgs(data['mp_guru_list'])
    xs = generate_initial_solution(data)    
    violations, vio_index = calc_violations(xs)
    # return xs
    indices = xs.index.to_list()
    niter = 0
    stuck = 0
    while violations != 0:
        niter += 1
        new_vio, vio_index = calc_violations(xs)
        if new_vio == 0:
            break
        a = random.choice(vio_index)
        b = mutate(xs, a)
        new_vio, _ = calc_violations(xs)
        if new_vio >= violations:
            swap_time(xs, b, a)
            stuck += 1
        else:
            violations = new_vio
            stuck = 0
        # if stuck > 20:
        #     print('anchor index')
        #     dup_h = xs.loc[a].hari
        #     dup_t0 = xs.loc[a].t0
        #     dup_t1 = xs.loc[a].t1
        #     print('duplicates')
        #     print(xs[ (xs['hari'] == dup_h) & (xs['t0'] == dup_t0) & (xs['t1'] == dup_t1) ])
        # if violations < 10:
        #     print(xs.loc[vio_index])
        #     input()
        # if violations < 5:
        #     break
        if violations == 0:
            break

        print(f"new_vio = {new_vio}")
    return xs


def main(data):
    data['mp_guru_list'] = _split_mpgs(data['mp_guru_list'])
    xs = _main(data)
    return xs
    # return xs.to_dict(orient='records')
    # result = []
    # for kelas, group in xs.groupby('kelas'):
    #     sub_res = { 
    #         'kelas': kelas,
    #         'items': group.sort_values(['hari', 't0', 't1']).to_dict(orient='records')
    #     }
    #     result.append(sub_res)
    # return result

# def test():
#     _data = [
#         []
#     ]
#     pd.DataFrame(result, columns=["kelas", "guru", "mp", "hari", "t0", "t1", 'jam'])

if __name__ == '__main__':
    with open('webapp/data_test.json') as f:
        data_1 = json.loads(f.read())
    with open('webapp/data_test_2.json') as f:
        data_2 = json.loads(f.read())
    result = main(data_1)