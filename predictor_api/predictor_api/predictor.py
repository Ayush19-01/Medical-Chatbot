import pickle
import pandas as pd
import numpy as np
from scipy.stats import mode
import spacy
import os
class Prediction:
    def __init__(self, symptoms=[]):
        self.symptoms = []
        self.u_symptoms = symptoms
        self.num_symptoms = [0] * 132
        self.symptom_index =  {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic_patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
        self.predictions_classes = np.array(['(vertigo) Paroymsal  Positional Vertigo', 'AIDS', 'Acne', 'Alcoholic hepatitis', 'Allergy', 'Arthritis', 'Bronchial Asthma', 'Cervical spondylosis', 'Chicken pox', 'Chronic cholestasis', 'Common Cold', 'Dengue', 'Diabetes', 'Dimorphic hemorrhoids(piles)', 'Drug Reaction', 'Fungal infection', 'GERD', 'Gastroenteritis', 'Heart attack', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Hypertension', 'Hyperthyroidism', 'Hypoglycemia', 'Hypothyroidism', 'Impetigo', 'Jaundice', 'Malaria', 'Migraine', 'Osteoarthristis', 'Paralysis (brain hemorrhage)', 'Peptic ulcer diseae', 'Pneumonia', 'Psoriasis', 'Tuberculosis', 'Typhoid', 'Urinary tract infection', 'Varicose veins', 'hepatitis A'])
        self.symptom_list = [i.replace("_"," ") for i in self.symptom_index.keys()]
        self.hidden_layer()
        print(self.symptoms)
        self.converter()

    def hidden_layer(self):
        #nlp = spacy.load('en_core_web_lg')
        nlp = spacy.load("fi_core_news_lg")
        for symptom in self.u_symptoms:
            doc = nlp(symptom)
            best_match = None
            best_score = 0
            for s in self.symptom_list:
                score = doc.similarity(nlp(s))
                if score > best_score:
                    best_match = s
                    best_score = score
            self.symptoms.append(best_match.replace(" ","_"))


    def converter(self):
        cleaned_symptoms = []
        for i in self.symptoms:
            tmp = i.strip()
            tmp = tmp.lower()
            tmp = tmp.replace(" ","_")
            cleaned_symptoms.append(tmp)

        for i in cleaned_symptoms:
            try:
                index = self.symptom_index[i]

            except KeyError:
                continue
            self.num_symptoms[index] = 1
        print(self.num_symptoms)
        self.num_symptoms = np.array(self.num_symptoms).reshape(1, -1)





    def predict(self):
        response_dic = {}
        rel_path=str(os.getcwd())
        nb_model = pickle.load(open(r'predictor_api\dataset\nb_model', 'rb'))
        rf_model = pickle.load(open(r'predictor_api\dataset\rf_model', 'rb'))
        svm_model = pickle.load(open(r'predictor_api\dataset\svm_model', 'rb'))
        rf_prediction = self.predictions_classes[rf_model.predict(self.num_symptoms)[0]]
        nb_prediction = self.predictions_classes[nb_model.predict(self.num_symptoms)[0]]
        svm_prediction = self.predictions_classes[svm_model.predict(self.num_symptoms)[0]]
        final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0][0]
        response_dic["Disease"] = final_prediction

        description = pd.read_csv(r'predictor_api\dataset\symptom_Description.csv', index_col='Disease')
        precaution = pd.read_csv(r'predictor_api\dataset\symptom_precaution.csv')
        precaution["Disease"] = precaution["Disease"].str.strip()
        precaution.fillna(0)
        # x = []
        # for i in description.iterrows():
        #     x.append(i[0])
        # x.sort()
        # print(x)
        response_dic["Description"] = description.loc[response_dic["Disease"]].values[0]
        pres = precaution.loc[precaution["Disease"] == response_dic["Disease"]]
        tmp = []
        for i in range(1, len(pres.values[0])):
            tmp.append(pres.values[0][i])
        response_dic["Precautions"] = tmp
        return response_dic



