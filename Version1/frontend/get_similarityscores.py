import pandas as pd
from typing import List, Optional
# from cv_analyzer import suggested_occupations
# from retrieve_occupations import occupation_lists


def clean_sentences(input_list):
    """
    Helper function to convert all entries in a list to strings if necessary.
    """
    return [str(sentence) for sentence in input_list]


def compute_similarity(sentences1: List[str], sentences2: List[str], model_name: Optional[str] = 'all-mpnet-base-v2') -> pd.DataFrame:
    from sentence_transformers import SentenceTransformer, util

    """
    Compute cosine similarity between two sets of sentences using a pre-trained SentenceTransformer model.

    Parameters:
    - sentences1 (List[str]): List of sentences for the first set.
    - sentences2 (List[str]): List of sentences for the second set.
    - model_name (Optional[str]): Name of the pre-trained model to use for sentence embedding. Defaults to 'all-mpnet-base-v2'.

    Returns:
    - pd.DataFrame: A DataFrame containing the cosine similarity scores between each pair of sentences.
    """
    # Validate input
    if not sentences1 or not sentences2:
        raise ValueError(
            "Both sentences1 and sentences2 must contain at least one sentence.")

    # Clean sentences (convert floats and other types to strings)
    sentences1 = clean_sentences(sentences1)
    sentences2 = clean_sentences(sentences2)

    # Load the pre-trained SBERT model
    model = SentenceTransformer(model_name)

    # Encode the sentences into embeddings
    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    # Calculate the cosine similarity between each pair of sentences
    similarity_scores = util.cos_sim(embeddings1, embeddings2)
    similarity_scores_list = similarity_scores.tolist()

    # Convert similarity scores to a DataFrame
    similarity_df = pd.DataFrame(
        similarity_scores_list, index=sentences1, columns=sentences2)

    return similarity_df


# Example usage
# similarity_results_df = compute_similarity(suggested_occupations, occupation_lists, model_name='all-mpnet-base-v2')
