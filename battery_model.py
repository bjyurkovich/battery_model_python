import scipy.io as spio
import numpy as np


def flatten(l): return [item for sublist in l for item in sublist]


def build_step_profile(config):
    profile = []
    for i in config:
        profile.append(np.linspace(i['val'], i['val'], i['time']))
    return flatten(profile)


class Battery:
    def __init__(self, soc0, dt):
        self.soc0 = soc0
        self.soc = self.soc0
        self.dt = dt
        self.vc1 = 0
        self.vc2 = 0

        mat = spio.loadmat('data/battery_mappings.mat', squeeze_me=True)
        self.ocv_map = np.array(mat['OCV_curve'])
        self.soc_map = np.linspace(0, 1, len(self.ocv_map))
        self.capacity = mat['capacity']

        self.ocv = self.calculate_ocv(self.soc)
        self.v_batt = self.ocv
        self.r0 = 0.001
        self.r1 = 0.0019
        self.r2 = 0.0014
        self.c1 = 10000
        self.c2 = 200000

    def calculate_soc(self, i):
        return self.soc + (-i / self.capacity / 3600) * self.dt

    def calculate_ocv(self, soc):
        return np.interp(soc, self.soc_map, self.ocv_map)

    def compute_vc1(self, i):
        beta = 1 / (self.r1 * self.c1)
        gamma = 1 / self.c1
        self.vc1 = np.exp(-beta * self.dt) * self.vc1 + gamma * - \
            i / beta * (1 - np.exp(-beta * self.dt))
        return self.vc1

    def compute_vc2(self, i):
        beta = 1 / (self.r2 * self.c2)
        gamma = 1 / self.c2
        self.vc2 = np.exp(-beta * self.dt) * self.vc2 + gamma * - \
            i / beta * (1 - np.exp(-beta * self.dt))
        return self.vc2

    def compute_timestep(self, i):
        self.soc = self.calculate_soc(i)
        self.ocv = self.calculate_ocv(self.soc)

        self.v_batt = self.ocv - i * self.r0 + \
            self.compute_vc1(i) + self.compute_vc2(i)

        return self.v_batt


b = Battery(0.5, 1)
c = b.capacity
profile = build_step_profile([
    {"val": -c * 0.5, "time": 100},
    {"val": 0, "time": 200},
    {"val": c * 3, "time": 200},
    {"val": 0, "time": 200},
    {"val": -c * 2, "time": 200},
    {"val": c * 2, "time": 100},
])

v_batt = np.zeros(len(profile))
soc = np.zeros(len(profile))

for n, i in enumerate(profile):
    v_batt[n] = b.compute_timestep(i)
    soc[n] = b.soc

print(v_batt)


spio.savemat('data/output.mat', {"soc": soc, "v_batt": v_batt, "u": profile})
