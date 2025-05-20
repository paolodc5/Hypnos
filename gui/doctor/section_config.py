def get_section_config(patient):
    # You need a mapping from doctor_id to surname for display
    # Let's assume patient.doctor_map is {doctor_id: surname}
    doctor_map = getattr(patient, "doctor_map", {})

    return {
        "Sleep": {
            "loader": patient.load_sleep_records,
            "items": lambda: sorted(patient.sleep_records, key=lambda r: r.date, reverse=True),
            "title": "🛌 Sleep Records",
            "fields_formatter": lambda r: [
                ("Date", r.date, ""),
                ("HR", r.hr, "bpm"),
                ("SpO₂", r.spo2, "%"),
                ("MovIdx", r.movement_idx, ""),
                ("Cycles", r.sleep_cycles, ""),
            ],
            "column_titles": ["Date", "HR", "SpO₂", "MovIdx", "Cycles"],
            "detail_formatter": lambda r: (
                f"Date: {r.date}\n"
                f"Device ID: {r.device_id}\n"
                f"HR: {r.hr} bpm\n"
                f"SpO₂: {r.spo2} %\n"
                f"Movement Index: {r.movement_idx}\n"
                f"Cycles: {r.sleep_cycles}\n"
                f"Patient ID: {r.patient_id}"
            )
        },
        "Notes": {
            "loader": patient.load_notes,
            "items": lambda: sorted(patient.doctor_notes, key=lambda n: n.date, reverse=True),
            "title": "📝 Notes",
            "fields_formatter": lambda n: [
                ("Date", n.date, ""),
                ("Doctor", n.doctor_id, ""),
                ("Preview", n.content[:40] + ("..." if len(n.content) > 40 else ""), ""),
            ],
            "column_titles": ["Date", "Doctor", "Preview"],
            "detail_formatter": lambda n: (
                f"Date: {n.date}\n"
                f"Doctor ID: {n.doctor_id}\n"
                f"Patient ID: {n.patient_id}\n"
                f"Note ID: {n.note_id}\n"
                f"Content:\n{n.content}"
            )
        },
        "Prescriptions": {
            "loader": patient.load_prescriptions,
            "items": lambda: sorted(patient.prescriptions, key=lambda p: p.precr_date, reverse=True),
            "title": "💊 Prescriptions",
            "fields_formatter": lambda p: [
                ("Date", p.precr_date, ""),
                ("Doctor", doctor_map.get(p.doctor_id, str(p.doctor_id)), ""),  # Show surname
                ("Type", p.treatm_type, ""),
                ("Preview", p.content[:30] + ("..." if len(p.content) > 30 else ""), ""),
            ],
            "column_titles": ["Date", "Doctor", "Type", "Preview"],
            "detail_formatter": lambda p: (
                f"Date: {p.precr_date}\n"
                f"Doctor: {doctor_map.get(p.doctor_id, str(p.doctor_id))}\n"
                f"Type: {p.treatm_type}\n"
                f"Patient ID: {p.patient_id}\n"
                f"Prescription ID: {p.prescription_id}\n"
                f"Content:\n{p.content}"
            )
        }
    }