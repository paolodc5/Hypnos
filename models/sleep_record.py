from typing import List, Optional
from statistics import mean


class SleepRecord:
    def __init__(self, 
                 date: str,
                 patient_id: int,
                 device_id: int,
                 hr: int,
                 spo2: float,
                 movement_idx: float,
                 sleep_cycles: str):
        self.date = date
        self.patient_id = patient_id
        self.device_id = device_id
        self.hr = hr
        self.spo2 = spo2
        self.movement_idx = movement_idx
        self.sleep_cycles = sleep_cycles  # You can parse this if you want a list

