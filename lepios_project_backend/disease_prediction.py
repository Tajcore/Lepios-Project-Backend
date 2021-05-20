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

    def predict_top3(self):
        classes = self.model.classes_
        out = self.model.predict_proba(self.input_table)[0]
        disease_prob = dict(zip(classes, out))
        sorted_diseases = [
            (k, v)
            for k, v in sorted(
                disease_prob.items(), key=lambda item: item[1], reverse=True
            )
            if v > 0
        ]
        return sorted_diseases[0:3]