from typing import List, Optional
from statistics import mean


class SleepRecord:
    def __init__(self, 
                 record_id: int, 
                 patient_id: int, 
                 doctor_id: int, 
                 date: str, 
                 duration: float):  # duration in hours
        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.duration = duration  # total time in bed (hours)

        # physiological data
        self.hr: List[int] = []
        self.hrv: List[float] = []
        self.sp02: List[int] = []

        # sleep stage times (in minutes)
        self.wake_up_time: float = 0.0
        self.REM_time: float = 0.0
        self.deep_sleep_time: float = 0.0
        self.light_sleep_time: float = 0.0

        # metrics
        self.efficiency: float = 0.0
        self.quality: str = "Unknown"
        self.quality_score: float = 0.0
        self.notes: Optional[str] = None

    def upload_data(self,
                    hr: List[int],
                    hrv: List[float],
                    sp02: List[int],
                    wake_up_time: float,
                    REM_time: float,
                    deep_sleep_time: float,
                    light_sleep_time: float):
        self.hr = hr
        self.hrv = hrv
        self.sp02 = sp02
        self.wake_up_time = wake_up_time
        self.REM_time = REM_time
        self.deep_sleep_time = deep_sleep_time
        self.light_sleep_time = light_sleep_time

        self.compute_sleep_score()

    def compute_sleep_score(self):
        if self.duration == 0:
            self.efficiency = 0
            self.quality = "Invalid"
            return

        total_sleep = self.REM_time + self.deep_sleep_time + self.light_sleep_time
        self.efficiency = round((total_sleep / (self.duration * 60)) * 100, 2)

        deep_ratio = self.deep_sleep_time / (self.duration * 60)
        rem_ratio = self.REM_time / (self.duration * 60)
        avg_hr = mean(self.hr) if self.hr else 75
        avg_hrv = mean(self.hrv) if self.hrv else 40
        spo2_drops = sum(1 for o2 in self.sp02 if o2 < 90)

        score = 0
        score += 0.30 * self.efficiency
        score += 0.15 * (deep_ratio * 100)
        score += 0.15 * (rem_ratio * 100)
        score += 0.15 * (max(0, min(100, 120 - avg_hr)) / 100) * 100
        score += 0.15 * min(100, avg_hrv)
        score += 0.10 * max(0, 100 - (spo2_drops * 5))

        self.quality_score = round(score, 2)

        if score >= 90:
            self.quality = "Excellent"
        elif score >= 75:
            self.quality = "Good"
        elif score >= 60:
            self.quality = "Fair"
        else:
            self.quality = "Poor"

    def __str__(self):
        return (f"SleepRecord(ID: {self.record_id}, Patient: {self.patient_id}, "
                f"Date: {self.date}, Score: {self.quality_score}, "
                f"Efficiency: {self.efficiency}%, Quality: {self.quality})")
