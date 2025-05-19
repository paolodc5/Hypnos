
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
        self.sleep_cycles = sleep_cycles
        self.duration = 7 ###### PAY ATTENTION TO THIS
        self.deep_sleep_time = 3 ##### PAY ATTENTION TO THIS
        self.light_sleep_time = 2 ##### PAY ATTENTION TO THIS
        self.REM_time = 1 ##### PAY ATTENTION TO THIS
        self.record_id = 3 ####### PAY ATTENTION TO THIS
        

 

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
    