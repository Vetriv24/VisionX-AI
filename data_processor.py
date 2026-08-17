import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MentalHealthDataProcessor:
    def __init__(self):
        self.survey_data = None
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.similarity_matrix = None
        
    def load_data(self, file_path):
        """Load and preprocess the mental health survey data"""
        self.survey_data = pd.read_csv(file_path)
        # Clean and preprocess the data
        self.survey_data['combined_text'] = self.survey_data.apply(
            lambda row: ' '.join(str(val) for val in row if pd.notna(val)), axis=1
        )
        
        # Create similarity matrix for matching
        tfidf_matrix = self.vectorizer.fit_transform(self.survey_data['combined_text'])
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
        
    def find_similar_cases(self, trauma_details, n=5):
        """Find similar cases from the survey data"""
        if self.survey_data is None:
            return []
            
        # Transform the input trauma details
        trauma_vector = self.vectorizer.transform([trauma_details])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(trauma_vector, self.vectorizer.transform(self.survey_data['combined_text']))
        
        # Get top similar cases
        top_indices = similarity_scores[0].argsort()[-n:][::-1]
        
        similar_cases = []
        for idx in top_indices:
            case = {
                'symptoms': self.survey_data.iloc[idx].to_dict(),
                'similarity_score': float(similarity_scores[0][idx])
            }
            similar_cases.append(case)
            
        return similar_cases
    
    def get_treatment_insights(self, trauma_details):
        """Get treatment insights based on similar cases"""
        similar_cases = self.find_similar_cases(trauma_details)
        
        insights = {
            'common_symptoms': [],
            'successful_treatments': [],
            'risk_factors': [],
            'recommended_duration': None
        }
        
        # Analyze similar cases to extract insights
        if similar_cases:
            # Extract common symptoms
            symptoms = [case['symptoms'].get('symptoms', '') for case in similar_cases]
            insights['common_symptoms'] = list(set(' '.join(symptoms).split()))
            
            # Extract successful treatments
            treatments = [case['symptoms'].get('treatment', '') for case in similar_cases]
            insights['successful_treatments'] = list(set(' '.join(treatments).split()))
            
            # Calculate recommended duration based on similar cases
            durations = [case['symptoms'].get('treatment_duration', 0) for case in similar_cases]
            insights['recommended_duration'] = int(np.mean(durations)) if durations else None
            
        return insights