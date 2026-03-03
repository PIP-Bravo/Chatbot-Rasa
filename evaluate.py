import pandas as pd
from rouge_score import rouge_scorer
from bert_score import score

df = pd.read_csv("response_rasa.csv", encoding="utf-8-sig", sep=",")
references = df['Groundtruth'].tolist()
candidates = df['bot_response'].tolist()

scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
rouge1_scores, rougeL_scores = [], []
for ref, cand in zip(references, candidates):
    scores = scorer.score(ref, cand)
    rouge1_scores.append(scores['rouge1'].fmeasure)
    rougeL_scores.append(scores['rougeL'].fmeasure)
df['ROUGE-1'] = rouge1_scores
df['ROUGE-L'] = rougeL_scores

P, R, F1 = score(candidates, references, lang="id", verbose=True)
df['BERTScore'] = F1.tolist()

print(df[['user_message','ROUGE-1','ROUGE-L','BERTScore']].head())
df.to_csv("evaluasi_chatbot.csv", index=False)
