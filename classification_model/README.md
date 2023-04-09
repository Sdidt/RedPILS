## RedPILS Classification Models

This folder contains the experiments and final results of the various classification models used. To view our final models and evaluation results, go through **Final Model Evaluation.ipynb**. Random seed has been fixed where possible, and results are reproducible with the exception of the Augemented Data Model that may show about 1% variance.

The below tables describe the functions of each file.

#### Python Notebooks

| File                                      | Purpose                                                                                     |
| ----------------------------------------- | ------------------------------------------------------------------------------------------- |
| Classification Model Experiments.ipynb    | Experiments for traditional classificaiton methods (SVMs, Random Forests, etc.)             |
| ML Classification Model Experiments.ipynb | Experiments for large ML models using BERT/RoBERTa based architectures                      |
| PCA+Sentiment Experiments.ipynb           | Experiments using dimensionality reduction and sentiment analysis models for classification |
| Final Model Evaluation.ipynb              | Final best models and their metrics on the 1k evaluation dataset                            |

#### Data Files

| File                                            | Purpose                                                                    |
| ----------------------------------------------- | -------------------------------------------------------------------------- |
| sampled_3000.csv                                | Raw data of 3000 comments sampled for hand-labeling                        |
| full_data.csv                                   | Hand-labeled 3000 comments                                                 |
| cleaned_full_data.csv                           | Hand-labeled data after preprocessing of text and scores                   |
| train_full.csv, eval_full.csv                   | Train-eval split (2000, 1000) of cleaned data                              |
| backup_before_reindex.json                      | Full 6679 raw data points from Solr                                        |
| full_6k_preds.csv                               | Final predictions of best model on all data                                |
| training_subset.csv, cleaned_subset.csv         | Temporary subsets of full data used during experiments, kept for reference |
| trained_subset_toxicity.csv                     | Data with toxicity scores from SenticNet API                               |
| siamese_embeddings.json, indian_sbert_preds.csv | Temporary result files from ML experiments                                 |
