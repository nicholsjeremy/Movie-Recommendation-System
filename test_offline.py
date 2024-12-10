import pytest
import pandas as pd
import os
from surprise import SVD, Dataset, Reader, accuracy
import time
from src.models.svdmodel import get_train_test_data

# Test offline evaluation
RMSE_THRESHOLD = 1.0
TRAINING_TIME_THRESHOLD = 1000 # seconds
INFERENCE_TIME_THRESHOLD = 0.1  # seconds per recommendation
MODEL_SIZE_THRESHOLD = 100  # MB

# ---- Fixtures ----
# @pytest.fixture
# def svd_model():
#     # Path to the pre-trained model file
#     model_file = 'svd.pkl'
#     return SVD.load(model_file), model_file

@pytest.fixture
def data():
    trainset, testset = get_train_test_data()
    return trainset, testset


# ---- Test Cases ----
# Pitfall: Detecting Label Leakage
def test_no_label_leakage(data):
    train_pairs = set((u[0], u[1]) for u in data[0].all_ratings())
    test_pairs = set((u[0], u[1]) for u in data[1])
    leakage = train_pairs.intersection(test_pairs)
    assert len(leakage) == 0, f"Label leakage detected with {len(leakage)} overlapping user-movie pairs"




# Pitfall: data dependencies
def test_no_data_dependencies(data):
    trainset = data[0]
    testset = data[1]
    train_users = set(trainset.all_users())  # List of all user IDs in the training set
    test_users = set([u for (u, _, _) in testset])  # Access user IDs directly from testset tuples
    user_dependency = test_users.intersection(train_users)
    # print(f"Number of overlapping users between train and test sets: {len(user_dependency)}")
    assert len(user_dependency) < len(test_users) * 0.1, f"High user dependency: {len(user_dependency)} overlapping users"


    train_movies = set(trainset.all_items())  # List of all movie IDs in the training set
    test_movies = set([i for (_, i, _) in testset])  # Access movie IDs directly from testset tuples
    movie_dependency = test_movies.intersection(train_movies)
    # print(f"Number of overlapping movies between train and test sets: {len(movie_dependency)}")
    assert len(movie_dependency) < len(test_movies) * 0.1, f"High movie dependency: {len(movie_dependency)} overlapping movies"



    # train_users = set([u[0] for u in data[0].all_users()])
    # test_users = set([u[0] for u in data[1]])
    # user_dependency = test_users.intersection(train_users)
    # assert len(user_dependency) < len(test_users) * 0.1, f"High user dependency: {len(user_dependency)} overlapping users"
    
    # train_movies = set([u[1] for u in data[0]])
    # test_movies = set([u[1] for u in data[1]])
    # movie_dependency = test_movies.intersection(train_movies)
    # assert len(movie_dependency) < len(test_movies) * 0.1, f"High movie dependency: {len(movie_dependency)} overlapping movies"
