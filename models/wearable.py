import random

# Here the wearable device class is defined.
# This class simulates a wearable device that generates sleep data.
# It includes methods to generate random heart rate, heart rate variability, ...

class WearableDevice:
    def __init__(self, device_id: int, model: str, patient_id: int):
        self.device_id = device_id
        self.model = model
        self.patient_id = patient_id

    def generate_sleep_data(self):
        hr = [random.randint(55, 70) for _ in range(100)]
        hrv = [random.uniform(30.0, 50.0) for _ in range(100)]
        sp02 = [random.randint(90, 99) for _ in range(100)]

        wake_up_time = random.uniform(20, 50)
        REM_time = random.uniform(70, 110)
        deep_sleep_time = random.uniform(80, 120)
        light_sleep_time = random.uniform(100, 150)

        return hr, hrv, sp02, wake_up_time, REM_time, deep_sleep_time, light_sleep_time