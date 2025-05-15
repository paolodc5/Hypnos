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
        self.latency: float = 0.0
        self.notes: Optional[str] = None

    def upload_data(self,
                    hr: List[int],
                    hrv: List[float],
                    sp02: List[int],
                    wake_up_time: float,
                    latency: float,
                    REM_time: float,
                    deep_sleep_time: float,
                    light_sleep_time: float):
        self.hr = hr
        self.hrv = hrv
        self.sp02 = sp02
        self.wake_up_time = wake_up_time
        self.latency = latency
        self.REM_time = REM_time
        self.deep_sleep_time = deep_sleep_time
        self.light_sleep_time = light_sleep_time

        self.compute_sleep_score()

    def compute_sleep_score(self):
        if self.duration == 0:
            self.efficiency = 0
            self.quality = "Invalid"
            self.latency = 0
            return

        total_sleep = self.REM_time + self.deep_sleep_time + self.light_sleep_time
        self.efficiency = round((total_sleep / (self.duration * 60)) * 100, 2)

        deep_ratio = self.deep_sleep_time / (self.duration * 60)
        rem_ratio = self.REM_time / (self.duration * 60)
        
        # Normalize total sleep: full score at 7h (420 min), min acceptable at 5h (300 min)
        sleep_score = max(0, min(1, (total_sleep - 300) / 120)) * 100
        rem_score = max(0, min(1, rem_ratio / 0.25)) * 100
        deep_score = max(0, min(1, deep_ratio / 0.2)) * 100
        
        if 10 <= self.latency <= 20:
            latency_score = 100
        elif self.latency < 10:
            latency_score = max(0, (self.latency - 2) / 8) * 100
        else:
            latency_score = max(0, 1 - (self.latency - 20) / 40) * 100

        score = 0
        score += 0.25 * sleep_score
        score += 0.25 * self.efficiency
        score += 0.20 * rem_score
        score += 0.20 * deep_score
        score += 0.10 * latency_score

        self.quality_score = round(score, 2)

        if score >= 90:
            self.quality = "Excellent"
        elif score >= 75:
            self.quality = "Good"
        elif score >= 60:
            self.quality = "Fair"
        else:
            self.quality = "Attention"

    def __str__(self):
        return (f"SleepRecord(ID: {self.record_id}, Patient: {self.patient_id}, "
                f"Date: {self.date}, Score: {self.quality_score}, "
                f"Efficiency: {self.efficiency}%, Quality: {self.quality})")
