# NoveltyChecker
NoveltyChecker is a powerful tool for assessing the novelty score of research manuscripts based on their titles and abstracts. This repository houses an application that utilizes the Scopus API to determine the uniqueness and innovation level of a manuscript. The novelty score ranges from 1 (worst) to 4 (best), providing valuable insights for researchers, editors, and peer reviewers.

## Key Features:
* **Scopus Integration:** NoveltyChecker seamlessly integrates with the Scopus API to gather information about published articles.
* **Abstract Similarity Analysis:** The application employs advanced algorithms to analyze the similarity between the manuscript abstract and existing articles on Scopus.
* **Search Count Evaluation:** NoveltyChecker considers the number of search results found via the Scopus API, providing an additional metric for assessing the manuscript's uniqueness.

## How It Works:
1. **Input Manuscript Information:** Users input the manuscript title and abstract into the application.
2. **Scopus API Integration:** The application connects to the Scopus API to retrieve relevant data on published articles.
3. **Novelty Score Calculation:** NoveltyChecker calculates the novelty score based on abstract similarity and the number of search results found on Scopus.
4. **Result Presentation:** Users receive a clear and concise report detailing the novelty score, allowing for quick and informed decision-making.
