from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Job
from users.views import user_profile

def get_job_recommendations(user_profile):
    # Assuming user_profile is a dictionary containing user skills and preferences
    user_skills = user_profile.get('skills', '')
    
    jobs = Job.objects.all()
    
    job_descriptions = [job.description for job in jobs]
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(job_descriptions)
    
    user_vector = tfidf_vectorizer.transform([user_skills])
    
    cosine_similarities = linear_kernel(user_vector, tfidf_matrix)
    
    similar_jobs = list(enumerate(cosine_similarities[0]))
    similar_jobs = sorted(similar_jobs, key=lambda x: x[1], reverse=True)
    
    recommended_jobs = [jobs[idx] for idx, _ in similar_jobs[:5]]  # Get top 5 recommendations
    
    return recommended_jobs
