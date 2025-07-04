from itertools import groupby

from sqlalchemy import select
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.models import Answer, Question, get_session
from src.settings import settings


def match_answer(question: str, session: Session) -> Answer | None:
    stmt = select(Question, Answer).join(Answer, Question.answer_id == Answer.id)
    results = session.execute(stmt).all()
    
    if not results:
        return None
    
    db_questions = []
    question_to_answer = {}
    
    for db_question, answer in results:
        db_questions.append(db_question.text)
        question_to_answer[db_question.text] = answer
    
    all_questions = db_questions + [question]
    
    vectorizer = TfidfVectorizer(
        analyzer="word", 
        # ngram_range=(1, 2),
        lowercase=True, 
    )
    tfidf_matrix = vectorizer.fit_transform(all_questions)
    
    user_question_vector = tfidf_matrix[-1]  # Last item is the user question
    db_question_vectors = tfidf_matrix[:-1]  # All except the last item
    
    similarities = cosine_similarity(user_question_vector, db_question_vectors).flatten()
    
    best_match_idx = similarities.argmax()
    best_similarity = similarities[best_match_idx]
    
    if best_similarity >= settings.similarity_threshold:
        best_question = db_questions[best_match_idx]
        return question_to_answer[best_question]
    
    return None



































































