import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from joblib import dump

data = pd.read_csv('data.csv')
# 2. Разделение данных
X = data['text']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Преобразование текста в TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 4. Обучение модели
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# 5. Оценка модели
y_pred = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

dump(vectorizer, "tfidf_vectorizer.joblib")
dump(model, "xss_detection_model.joblib")
print("Модель и векторизатор успешно сохранены!")
