from situation.predict_dialog_act_type import PredictDialogActType


pa = PredictDialogActType("situation_predicter", is_base_situation=True)
print(pa.predict_da("今日の夜飯行かね？"))
