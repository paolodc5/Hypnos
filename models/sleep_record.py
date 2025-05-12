from typing import Optional, List
from statistics import mean
from models.wearable import Wearable

class SleepRecord:
    def __init__(self, record_id: int, patient_id: int, doctor_id: int, date: str, duration: float, efficiency: float, quality: str, notes: Optional[str] = None):
        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
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

    def upload_data(self, hr: List[int], hrv: List[float], sp02: List[int], wake_up_time: float, REM_time: float, deep_sleep_time: float, light_sleep_time: float):
        self.hr = hr
        self.hrv = hrv
        self.sp02 = sp02
        self.wake_up_time = wake_up_time
        self.REM_time = REM_time
        self.deep_sleep_time = deep_sleep_time
        self.light_sleep_time = light_sleep_time

        self.compute_sleep_quality()

    def compute_sleep_score(self):
        if self.duration == 0:
            self.efficiency = 0
            self.quality = "Invalid"
            return
        
        total_sleep_time = ((self.REM_time or 0)+(self.deep_sleep_time or 0)+(self.light_sleep_time or 0))
        self.efficiency = round((total_sleep_time / self.duration*60) * 100, 2)

        deep_ratio = self.deep_sleep_time / self.duration*60
        rem_ratio = self.REM_time / self.duration*60
        avg_hr = mean(self.hr) if self.hr else 75
        avg_hrv = mean(self.hrv) if self.hrv else 40
        spo2_drops = sum(1 for o2 in self.sp02 if o2 < 90) if self.sp02 else 0

        score = 0
        score += 0.30 * self.efficiency                           # up to 30 points
        score += 0.15 * (deep_ratio * 100)                        # up to 15 points
        score += 0.15 * (rem_ratio * 100)                         # up to 15 points
        score += 0.15 * max(0, min(100, (120 - avg_hr))) / 100 * 100   # up to 15 points (lower HR better)
        score += 0.15 * min(100, avg_hrv)                         # up to 15 points (higher HRV better)
        score += 0.10 * max(0, 100 - (spo2_drops * 5))            # up to 10 points (each drop costs 5 pts)

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
        return f"SleepRecord({self.record_id}, Patient ID: {self.patient_id}, Date: {self.date}, Duration: {self.duration} hours, Efficiency: {self.efficiency}%, Quality: {self.quality})"
    