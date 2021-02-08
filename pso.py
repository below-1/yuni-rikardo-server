import random
import numpy as np
import numpy.ma as ma

KELAS = [{"id":1,"nama":"VIIA"},{"id":2,"nama":"VIIB"},{"id":3,"nama":"VIIC"},{"id":4,"nama":"VIID"},{"id":5,"nama":"VIIE"},{"id":6,"nama":"VIIF"},{"id":7,"nama":"VIIG"},{"id":8,"nama":"VIIH"},{"id":9,"nama":"VIII"},{"id":10,"nama":"VIIJ"},{"id":11,"nama":"VIIK"}]
N_KELAS = len(KELAS)
MP_GURU = [{"guru_nama":"batsyeba poyk, S.Th","mp_nama":"agama","id":1,"bobot":3,"mp_id":1,"guru_id":1},{"guru_nama":"Sinyonaris Lonakoni, S.Pd","mp_nama":"agama","id":2,"bobot":3,"mp_id":1,"guru_id":2},{"guru_nama":"Onita Jumiati Hauteas, S.Pd","mp_nama":"agama","id":3,"bobot":3,"mp_id":1,"guru_id":3},{"guru_nama":"Welhelmus Willa, S.Pd","mp_nama":"bahasa indonesia","id":4,"bobot":6,"mp_id":2,"guru_id":4},{"guru_nama":"Benediktus Tnesi, S.Pd","mp_nama":"bahasa indonesia","id":5,"bobot":6,"mp_id":2,"guru_id":5},{"guru_nama":"Apriliani M. Tewan, S.Pd","mp_nama":"bahasa indonesia","id":6,"bobot":6,"mp_id":2,"guru_id":6},{"guru_nama":"Vera R. Menno","mp_nama":"bahasa indonesia","id":7,"bobot":6,"mp_id":2,"guru_id":7},{"guru_nama":"Mafrudo, S.Pd","mp_nama":"matematika","id":8,"bobot":5,"mp_id":4,"guru_id":8},{"guru_nama":"Fransiska G.N. Jebarus, S.Pd","mp_nama":"matematika","id":9,"bobot":5,"mp_id":4,"guru_id":9},{"guru_nama":"Regina Dusut, S.Pd","mp_nama":"matematika","id":10,"bobot":5,"mp_id":4,"guru_id":10},{"guru_nama":"Mariana Dimu, S.Pd","mp_nama":"pkn","id":11,"bobot":3,"mp_id":3,"guru_id":11},{"guru_nama":"Welhelmus Willa, S.Pd","mp_nama":"pkn","id":12,"bobot":3,"mp_id":3,"guru_id":4},{"guru_nama":"Juliana Kota, S.Pd","mp_nama":"pkn","id":13,"bobot":3,"mp_id":3,"guru_id":12},{"guru_nama":"Erna Maria A. Bone, S.Pd","mp_nama":"ips","id":14,"bobot":4,"mp_id":5,"guru_id":13},{"guru_nama":"Bulan Banaweng, S.Pd","mp_nama":"ips","id":15,"bobot":4,"mp_id":5,"guru_id":14},{"guru_nama":"Johana J. Payk","mp_nama":"ips","id":16,"bobot":4,"mp_id":5,"guru_id":15},{"guru_nama":"Johana J. Payk","mp_nama":"ips","id":17,"bobot":4,"mp_id":5,"guru_id":15},{"guru_nama":"Selviana Lekbia","mp_nama":"ips","id":18,"bobot":4,"mp_id":5,"guru_id":16},{"guru_nama":"Reefjhon M. Dida","mp_nama":"bahasa inggris","id":19,"bobot":4,"mp_id":6,"guru_id":17},{"guru_nama":"Erwina Agustina","mp_nama":"bahasa inggris","id":20,"bobot":4,"mp_id":6,"guru_id":18},{"guru_nama":"Antoheta M. Bisinglasi","mp_nama":"bahasa inggris","id":21,"bobot":4,"mp_id":6,"guru_id":19},{"guru_nama":"Febriani N. F. Maikameng","mp_nama":"ipa","id":22,"bobot":5,"mp_id":7,"guru_id":20},{"guru_nama":"Rosalina Isabela","mp_nama":"ipa","id":23,"bobot":5,"mp_id":7,"guru_id":21},{"guru_nama":"Merry A. Prasetya","mp_nama":"ipa","id":24,"bobot":5,"mp_id":7,"guru_id":22},{"guru_nama":"Ham Engel Dami","mp_nama":"pjkr","id":25,"bobot":3,"mp_id":8,"guru_id":23},{"guru_nama":"Jacky Pong","mp_nama":"pjkr","id":26,"bobot":3,"mp_id":8,"guru_id":24},{"guru_nama":"Johana J. Payk","mp_nama":"prakarya","id":27,"bobot":2,"mp_id":9,"guru_id":15},{"guru_nama":"batsyeba poyk, S.Th","mp_nama":"prakarya","id":28,"bobot":2,"mp_id":9,"guru_id":1},{"guru_nama":"Sofia Mesakh","mp_nama":"prakarya","id":29,"bobot":2,"mp_id":9,"guru_id":25},{"guru_nama":"Agustinus Epu","mp_nama":"seni budaya","id":30,"bobot":3,"mp_id":10,"guru_id":26},{"guru_nama":"Selviana Lekbia","mp_nama":"seni budaya","id":31,"bobot":3,"mp_id":10,"guru_id":27},{"guru_nama":"Frederika Tamar Karmaley","mp_nama":"seni budaya","id":32,"bobot":3,"mp_id":10,"guru_id":28},{"guru_nama":"Samaria Sandi","mp_nama":"bp/bk","id":33,"bobot":2,"mp_id":11,"guru_id":29}]
BOBOT_HARI = [ { "hari": 0, "max": 7 }, { "hari": 1, "max": 8 }, { "hari": 2, "max": 8 }, { "hari": 3, "max": 7 }, { "hari": 4, "max": 5 }, { "hari": 5, "max": 5 }]
THRESHOLD = 20

def pso(args):
    global BOBOT_HARI
    KELAS = args['kelas']
    MP_GURU = args['mp_guru']
    N_KELAS = len(KELAS)
    N_HOURS = 40
    N_PARTICLES = args['n_particles']
    THRESHOLD = args['threshold']
    W = args['w']
    C1 = args['c1']
    C2 = args['c2']

    tmp_mp_guru = []
    mp_guru_id = 1
    for mp_guru in MP_GURU:
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

    MP_GURU = [*tmp_mp_guru]

    MAP_MP_LENGTH = {}
    for mp in MP_GURU:
        if mp["jam"] not in MAP_MP_LENGTH:
            MAP_MP_LENGTH[mp["jam"]] = list()
        MAP_MP_LENGTH[mp["jam"]].append(mp["id"])


    # return { "message": "OK" }

    class KelasSolutionGenerator:
        def __init__(self):
            self.exists = set()

        def _generate_for_day(self, day):
            day_data = BOBOT_HARI[day]
            max_bobot = day_data["max"]
            nmp = 0

            # Excluding
            sample_mp_guru = random.sample(MP_GURU, 2 if nmp % 2 == 0 else 3)
            sample_total_hours = sum(mp_guru["jam"] 
                for mp_guru in sample_mp_guru
            )
            id_mp_guru = set(mp_guru["id"] for mp_guru in sample_mp_guru)
            redundant = len( id_mp_guru.intersection(self.exists) ) > 0
            while sample_total_hours != max_bobot or redundant:
                sample_mp_guru = random.sample(MP_GURU, 2 if nmp % 2 == 0 else 3)
                id_mp_guru = set(mp_guru["id"] for mp_guru in sample_mp_guru)
                redundant = len( id_mp_guru.intersection(self.exists) ) > 0
                sample_total_hours = sum(mp["jam"] for mp in sample_mp_guru)
                nmp += 1
            for r in sample_mp_guru:
                self.exists.add(r["id"])
            # print(f"day={day}")
            # print(f"target={max_bobot}")
            # print(sample_mp_guru)
            # input()
            result = []
            for sm in sample_mp_guru:
                for i in range(sm["jam"]):
                    result.append(sm["id"])
            return result

        def generate(self):
            result = []
            for day in range(6):
                day_solution = self._generate_for_day(day)
                # print(f"hari-{day}")
                print_schedule(day_solution)
                # print()
                # print(f"day-{day}")
                # print(sum(ds["bobot"] for ds in day_solution))
                # print(self.exists)
                result.extend(day_solution)
            return result

    def print_schedule(schedule):
        for id in schedule:
            data, *_ = [ mp_guru for mp_guru in MP_GURU if mp_guru["id"] == id ]

    # def print_schedule_2(mp_id):
    #     guru = next(mp for mp in MP_GURU if mp["id"] == mp_id)
    #     print(guru)

    def generate_initial_solution(n=10):
        particles = []
        for i in range(n):
            particle = []
            for kelas in KELAS:
                kelas_jadwal_generator = KelasSolutionGenerator();
                kelas_result = kelas_jadwal_generator.generate()
                particle.append(kelas_result)
            particles.append(particle)
        return np.array(particles)
            # print_schedule(kelas_result)
            # print(kelas_result)

    def find_guru_by_mp_id(mp_id):
        guru, *_ = [ mp["guru_id"] for mp in MP_GURU if mp["id"] == mp_id ]
        return guru

    def find_guru(mp_id):
        guru = next(mp for mp in MP_GURU if mp["id"] == mp_id)
        return guru

    def _transform_to_guru(particles):
        # Contraint 1: Tabrakan guru
        N_KELAS = len(KELAS)
        guru = []
        for i in range(N_PARTICLES):
            particle = []
            for j in range(N_KELAS):
                kelas = [ find_guru_by_mp_id(x) for x in particles[i, j] ]
                particle.append(kelas)
            guru.append(particle)
        # print(guru)
        # return guru
        return np.array(guru)

    def calculate_violations(particles):
        # Contraint 1: Tabrakan guru
        N_KELAS = len(KELAS)
        violations = []
        for i in range(N_PARTICLES):
            particle = []
            for j in range(N_HOURS):
                kelas = [ find_guru_by_mp_id(x) for x in particles[i, :, j] ]
                xs = []
                for x in kelas:
                    just_x = [ y for y in kelas if y == x ]
                    if len(just_x) == 1:
                        xs.append(0)
                    else:
                        xs.append(1)
                particle.append(xs)
            particle = np.array(particle)
            particle = np.matrix.transpose(particle)
            violations.append(particle)
        # print(guru)
        # return guru
        return np.array(violations)

    def calc_vio_fit(particles):
        guru_jadwal = _transform_to_guru(particles)
        violations = calculate_violations(particles)
        fitness = np.array([ violations[i].sum() for i in range(N_PARTICLES) ])
        return violations, fitness

    particles = generate_initial_solution(n=N_PARTICLES)
    count_iter = 0
    local_best_fitness = np.array([ 10000 for i in range(N_PARTICLES) ])
    trials = np.zeros((N_PARTICLES, ), dtype=int)
    while True:
    #     # print(particles)
        violations, fitness = calc_vio_fit(particles)
        # print(violations)
        # print(fitness)
        # break
        min_fit = min(fitness)
        min_i = next(i for i, j in enumerate(fitness) if j == min_fit)
        particle = particles[min_i]

        local_best = np.copy(particles)
        _, local_best_fitness = calc_vio_fit(local_best)
        global_best = np.copy(particles[min_i]).reshape(N_KELAS, N_HOURS)

        for i in range(N_PARTICLES):
            vio_per_kel = violations.sum(axis=0).sum(axis=1)
            j = np.argmax(vio_per_kel)
            violated_indices = np.where(violations[i, j] == 1)[0]
            if len(violated_indices) == 0:
                continue
            k = violated_indices[0]
            neighbours = [k]

            if particles[i, j, k + 1] == particles[i, j, k]:
                neighbours.append(k + 1)
            if (k < N_HOURS - 2) and particles[i, j, k + 2] == particles[i, j, k]:
                neighbours.append(k + 2)

            if len(neighbours) == 1:
                continue

    #         # find mp_guru with same length
            pools = MAP_MP_LENGTH[len(neighbours)]

            upd_indx = int((abs(W * particles[i, j, k] \
                + (C1 *  random.random() * local_best[i, j, k] - particles[i, j, k]) \
                + (C2 * random.random() * global_best[j, k] - particles[i, j, k]))) % len(pools))
            updated_velocity = pools[upd_indx]

            if 1 in set(violations[i, j, neighbours]):
                particles[i, j, neighbours] = updated_velocity

        violations, fitness = calc_vio_fit(particles)
        max_fit = max(fitness)
        max_i = [i for i, j in enumerate(fitness) if j == max_fit]
        global_best = np.copy(particles[max_i])

        print(f"fitness: {fitness}")
        print(f"local_best_fitness: {local_best_fitness}")
        print(f"trials: {trials}")

        for i in range(N_PARTICLES):
            if fitness[i] < local_best_fitness[i]:
                local_best[i, :] = particles[i, :]
                trials[i] = 0
            else:
                trials[i] += 1

            if trials[i] > THRESHOLD:
                # reset particles[i]
                kelas_jadwal_generator = KelasSolutionGenerator();
                kelas_result = kelas_jadwal_generator.generate()
                particles[i] = np.array(kelas_result)
                trials[i] = 0

            # print()
            # print(f"trials: {trials}")
            # print(f"fitness: {fitness}")
            # print(f"local_best_fitness: {local_best_fitness}")

        if len(np.where(fitness == 0)[0]) != 0:
            break

        count_iter += 1

    particle_index = (np.where(fitness == 0)[0])[0]
    # print(particle_index)
    particle = particles[particle_index]
    # for i in range(N_PARTICLES):
    result = []
    for j in range(N_KELAS):
        subres = []
        for k in range(N_HOURS):
            subres.append(find_guru(particle[j, k]))
        result.append(subres)

    return result