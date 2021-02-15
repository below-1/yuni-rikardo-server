import random
import numpy as np
import numpy.ma as ma
import time
import json

from collections import namedtuple

PoolItem = namedtuple('PoolItem', ['mp_id', 'jam', 'mpg', 'id'])

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
        # if self.mark == 2:
        # print(f"size of mp_guru_list: {len(self.mp_guru_list)}")
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
                for item in day_result:
                    current_mp_hours[item.mp_id] += item.jam
                    if current_mp_hours[item.mp_id] == mp_hours[item.mp_id]:
                        pools = [ it for it in pools if item.mp_id != it.mp_id ]
                result.append(day_result)
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
        result.append(kelas_result)
    return result

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

if __name__ == '__main__':
    with open('webapp/data_test.json') as f:
        data = json.loads(f.read())
    data['mp_guru_list'] = _split_mpgs(data['mp_guru_list'])
    init_sols = generate_initial_solution(data)
    # spreaded = spread_solutions(init_sols)
    # print(spreaded)

    # generator = KelasSolutionGenerator(mark=1, **data)
    # kelas_result = generator.generate()
    # print('first kelas')

    # generator = KelasSolutionGenerator(mark=2, **data)
    # kelas_result = generator.generate()
    # print('second kelas')