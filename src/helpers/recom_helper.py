def preprocess_data(documents):
    data = []
    for doc in documents:
        text = doc["title"]
        for step in doc.get("steps", []):
            for product in step.get("products", []):
                text += ", " + product["description"]
        data.append(text)
    return data
