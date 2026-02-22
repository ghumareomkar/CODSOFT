import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# ---------------- DATA LOADER ---------------- #

class DataLoader:
    def __init__(self, ratings_path, movies_path):
        self.ratings = pd.read_csv(ratings_path)
        self.movies = pd.read_csv(movies_path)

    def get_user_item_matrix(self):
        matrix = self.ratings.pivot_table(
            index='user_id',
            columns='movie_id',
            values='rating'
        )
        return matrix.fillna(0)


# ---------------- COLLABORATIVE FILTERING ---------------- #

class CollaborativeFiltering:
    def __init__(self, user_item_matrix, movies_df):
        self.matrix = user_item_matrix
        self.movies = movies_df

    def user_based_recommend(self, user_id, top_n=5):
        if user_id not in self.matrix.index:
            return None

        similarity = cosine_similarity(self.matrix)
        sim_df = pd.DataFrame(similarity,
                              index=self.matrix.index,
                              columns=self.matrix.index)

        similar_users = sim_df[user_id].sort_values(ascending=False)[1:6]

        weighted_ratings = np.zeros(self.matrix.shape[1])
        sim_sum = similar_users.sum()

        if sim_sum == 0:
            return None

        for sim_user, score in similar_users.items():
            weighted_ratings += self.matrix.loc[sim_user] * score

        predicted_ratings = weighted_ratings / sim_sum
        recommendations = pd.Series(predicted_ratings,
                                    index=self.matrix.columns)

        rated_items = self.matrix.loc[user_id]
        recommendations = recommendations[rated_items == 0]

        top_items = recommendations.sort_values(ascending=False).head(top_n)

        return self._format_output(top_items)

    def item_based_recommend(self, user_id, top_n=5):
        if user_id not in self.matrix.index:
            return None

        similarity = cosine_similarity(self.matrix.T)
        sim_df = pd.DataFrame(similarity,
                              index=self.matrix.columns,
                              columns=self.matrix.columns)

        user_ratings = self.matrix.loc[user_id]
        scores = pd.Series(np.zeros(len(self.matrix.columns)),
                           index=self.matrix.columns)

        for item, rating in user_ratings.items():
            if rating > 0:
                scores += sim_df[item] * rating

        scores = scores[user_ratings == 0]
        top_items = scores.sort_values(ascending=False).head(top_n)

        return self._format_output(top_items)

    def _format_output(self, recommendations):
        results = []
        for movie_id, score in recommendations.items():
            title = self.movies[self.movies['movie_id'] == movie_id]['title'].values[0]
            results.append((title, round(score, 2)))
        return results


# ---------------- CONTENT-BASED FILTERING ---------------- #

class ContentBasedFiltering:
    def __init__(self, movies):
        self.movies = movies
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(movies['genre'])
        self.similarity = cosine_similarity(self.tfidf_matrix)

    def recommend(self, movie_title, top_n=5):
        movie_title = movie_title.lower().strip()

        matches = self.movies[
            self.movies['title'].str.lower().str.contains(movie_title)
        ]

        if matches.empty:
            suggestions = self.movies['title'].head(5).tolist()
            return f"Movie not found. Try one of these: {suggestions}"

        idx = matches.index[0]

        sim_scores = list(enumerate(self.similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

        movie_indices = [i[0] for i in sim_scores]

        return self.movies.iloc[movie_indices][['title', 'genre']]


# ---------------- HYBRID SYSTEM ---------------- #

class HybridRecommender:
    def __init__(self, ratings_path, movies_path):
        loader = DataLoader(ratings_path, movies_path)
        self.movies = loader.movies
        self.matrix = loader.get_user_item_matrix()

        self.cf = CollaborativeFiltering(self.matrix, self.movies)
        self.cb = ContentBasedFiltering(self.movies)

    def recommend_for_user(self, user_id):
        print("\n🔹 USER-BASED COLLABORATIVE FILTERING:")
        user_based = self.cf.user_based_recommend(user_id)

        if user_based:
            for title, score in user_based:
                print(f"{title}  |  Predicted Score: {score}")
        else:
            print("No recommendations available.")

        print("\n🔹 ITEM-BASED COLLABORATIVE FILTERING:")
        item_based = self.cf.item_based_recommend(user_id)

        if item_based:
            for title, score in item_based:
                print(f"{title}  |  Score: {score}")
        else:
            print("No recommendations available.")

    def recommend_similar_movie(self, title):
        print("\n🔹 CONTENT-BASED RECOMMENDATIONS:")
        result = self.cb.recommend(title)
        print(result)


# ---------------- MAIN INTERFACE ---------------- #

if __name__ == "__main__":
    system = HybridRecommender("ratings_large.csv", "movies_large_named.csv")

    while True:
        print("\n1. Recommend for User")
        print("2. Recommend Similar Movies")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            try:
                uid = int(input("Enter User ID: "))
                system.recommend_for_user(uid)
            except:
                print("Invalid User ID.")
        elif choice == "2":
            title = input("Enter Movie Title: ")
            system.recommend_similar_movie(title)
        elif choice == "3":
            print("Exiting system.")
            break
        else:
            print("Invalid choice.")

# Enter in output > 2 > Love 
# It will recommend related movies