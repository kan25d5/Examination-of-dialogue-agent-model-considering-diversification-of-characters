from situation.predict_situation import PredictSituation


ps = PredictSituation("situation_predicter", is_base_situation=True)
print(ps.predict_situation("今日の夜飯行かね？"))
