from model_service_gru import predict_burnout

# HISTORY (terakumulasi selama sesi berjalan)
work_hours_history    = []
sleep_hours_history   = []
burnout_score_history = []

# HELPER INPUT
def input_float(prompt, min_val, max_val):
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"  ⚠ Masukkan angka antara {min_val} dan {max_val}.")
        except ValueError:
            print("  ⚠ Input tidak valid, masukkan angka.")

# MAIN LOOP
print("=" * 50)
print("   BURNOUT PREDICTOR — Input Harian")
print("=" * 50)
print("Ketik 'q' kapan saja untuk keluar.\n")

hari_ke = 1

while True:
    print(f"\n--- Hari ke-{hari_ke} ---")

    raw = input("Lanjut input hari ini? (Enter untuk lanjut / q untuk keluar): ").strip().lower()
    if raw == "q":
        print("\nSampai jumpa!")
        break

    work_hours          = input_float("Jam kerja hari ini  (0-24): ", 0, 24)
    sleep_hours         = input_float("Jam tidur malam ini (0-24): ", 0, 24)
    questionnaire_score = input_float("Skor kuesioner burnout (0-100): ", 0, 100)

    # Prediksi pakai history SEBELUM hari ini ditambahkan
    result = predict_burnout(
        work_hours_list     = work_hours_history,
        sleep_hours_list    = sleep_hours_history,
        burnout_score_list  = burnout_score_history,
        questionnaire_score = questionnaire_score
    )
    # Jalankan prediksi
    result = predict_burnout(
        work_hours_list     = work_hours_history,
        sleep_hours_list    = sleep_hours_history,
        burnout_score_list  = burnout_score_history,
        questionnaire_score = questionnaire_score
    )

    # Baru tambah ke history SETELAH prediksi
    work_hours_history.append(work_hours)
    sleep_hours_history.append(sleep_hours)
    burnout_score_history.append(result["final_burnout_score"])

    # TAMPILKAN HASIL
    print("\n" + "=" * 50)
    print("  HASIL PREDIKSI")
    print("=" * 50)

    if result["behavior_prediction_score"] is not None:
        print(f"  Skor prediksi perilaku : {result['behavior_prediction_score']}")
    print(f"  Skor kuesioner         : {result['questionnaire_score']}")
    print(f"  Skor burnout akhir     : {result['final_burnout_score']}")
    print(f"  Level burnout          : {result['final_burnout_level']}")

    if result["difference"] is not None:
        print(f"  Selisih                : {result['difference']}")
        print(f"  Metode pembobotan      : {result['weighting_type']}")

    print(f"  Catatan                : {result['note']}")

    tw = result["trend_warning"]
    print(f"\n  [Tren] {tw['warning']}")
    if tw["avg_delta"] is not None:
        arah = "+" if tw["avg_delta"] > 0 else ""
        print(f"  Rata-rata perubahan    : {arah}{tw['avg_delta']} poin/hari")
        print(f"  Streak naik            : {tw['streak_up']} hari")

    print("=" * 50)

    hari_ke += 1
