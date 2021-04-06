class DiseasePrediction:
    def __init__(self, model, input_table):
        self.model = model
        self.input_table = input_table

    def clear_input(self):
        for col in self.input_table.columns:
            self.input_table[col].values[:] = 0.0

    def input_symptoms(self, symptoms):
        self.clear_input()
        for symptom in symptoms:
            symptom_fixed = " " + symptom
            if symptom_fixed in self.input_table.columns:
                self.input_table[symptom_fixed].values[:] = 1.0

    def predict(self):
        return self.model.predict(self.input_table)[0]