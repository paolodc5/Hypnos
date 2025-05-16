from typing import Optional, List
from statistics import mean
from models.wearable import WearableDevice

class SleepRecord:
    def __init__(self, 
                 record_id: int, 
                 patient_id: int, 
                 device_id: int, 
                 date: str, 
                 duration: float, 
                 efficiency: float, 
                 quality: str, 
                 notes: Optional[str] = None):
        self.record_id = record_id
        self.patient_id = patient_id
        self.device_id = device_id
        self.date = date
        
        self.duration = duration  # Duration in hours
        self.efficiency = efficiency  # Sleep efficiency percentage (amount of time asleep vs. time in bed)
        self.quality = quality  # Sleep quality rating (e.g., "Good", "Fair", "Poor")
        
        self.hr = List[int] = [] # Heart rate during sleep (optional)
        self.hrv = List[float] = [] # Heart rate variability during sleep (optional)
        self.sp02 = List[int] = [] # SpO2 levels during sleep (optional)
        self.wake_up_time = float # Wake-up time in minutes (optional)
        self.REM_time = float # REM sleep time in minutes (optional)
        self.deep_sleep_time = float # Deep sleep time in minutes (optional)
        self.light_sleep_time = float # Light sleep time in minutes (optional)

        self.notes = notes  # Additional notes about the sleep record

    def require_data(self, hr: List[int], hrv: List[float], sp02: List[int], latency: float, wake_up_time: float, REM_time: float, deep_sleep_time: float, light_sleep_time: float):
        self.hr = hr
        self.hrv = hrv
        self.sp02 = sp02
        self.latency = latency
        self.wake_up_time = wake_up_time
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
        
        total_sleep_time = ((self.REM_time or 0)+(self.deep_sleep_time or 0)+(self.light_sleep_time or 0))
        self.efficiency = round((total_sleep_time / self.duration*60) * 100, 2)

        # Normalize total sleep: full score at 7h (420 min), min acceptable at 5h (300 min)
        sleep_score = max(0, min(1, (total_sleep_time - 300) / 120)) * 100
        rem_score = max(0, min(1, rem_ratio / 0.25)) * 100

        deep_ratio = self.deep_sleep_time / self.duration*60
        rem_ratio = self.REM_time / self.duration*60
        deep_score = max(0, min(1, deep_ratio / 0.2)) * 100

        if 10 <= self.latency <= 20:
            latency_score = 100
        elif self.latency < 10:
            latency_score = max(0, (self.latency - 2) / 8) * 100  # scaled 2–10 min
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
        return f"SleepRecord({self.record_id}, Patient ID: {self.patient_id}, Date: {self.date}, Duration: {self.duration} hours, Efficiency: {self.efficiency}%, Quality: {self.quality})"
    