from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Job
from users.models import User  # Make sure you're importing the User model correctly

def get_job_recommendations(user_profile):
    user_skills = user_profile.get('skills', '')
    user_preferences = user_profile.get('preferences', '')  # Adjust the key based on your user profile data
    
    jobs = Job.objects.all()
    
    job_descriptions = [job.description for job in jobs]
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(job_descriptions)
    
    user_vector = tfidf_vectorizer.transform([user_skills + " " + user_preferences])  # Combine skills and preferences
    
    cosine_similarities = linear_kernel(user_vector, tfidf_matrix)
    
    similar_jobs = list(enumerate(cosine_similarities[0]))
    similar_jobs = sorted(similar_jobs, key=lambda x: x[1], reverse=True)
    
    recommended_jobs = [jobs[idx] for idx, _ in similar_jobs[:5]]  # Get top 5 recommendations
    
    return recommended_jobs

