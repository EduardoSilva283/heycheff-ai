from src.recommendation.recomBERT import get_bert_recommendations
from src.recommendation.recomendacao import get_recommendations

if __name__ == '__main__':
    recommendations = get_recommendations("Camarão")

    print("Recomendação de Camarão com Vetorização\n")
    for rec, score in recommendations:
        print(f"Receita: {rec} Similaridade: {score:.2f}")

    bert_recommendations = get_bert_recommendations("Hamburger")

    print("\nRecomendação de Hamburger com BERT\n")
    for rec, score in bert_recommendations:
        print(f"Receita: {rec} Similaridade: {score:.4f}")
