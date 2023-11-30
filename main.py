import json
from duckduckgo_search import DDGS

# Загрузка данных из файла JSON
try:
    with open('data.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
except FileNotFoundError:
    json_data = {"queries": []}


def save_data():
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=2)


def search_json(query):
    matching_answers = []

    # First, search for exact matches in queries
    for item in json_data["queries"]:
        if any(q.lower() == query.lower() for q in item["queries"]):
            matching_answers.append(item["answer"])

    # If no exact matches found, search for words in the query within answers
    if not matching_answers:
        for item in json_data["queries"]:
            if any(word.lower() in item["answer"].lower() for word in query.split()):
                matching_answers.append(item["answer"])

    if matching_answers:
        return matching_answers
    else:
        return "No matching answer found."


def add_custom_data():
    print("Введите один или несколько запросов через запятую. После поставьте точку и напишите ваш ответ.")
    user_input = input("Пример: кошки, коты, котики. Кошки - это такие-то животные\n")

    parts = user_input.split(".")
    if len(parts) == 2:
        queries = [q.strip() for q in parts[0].split(",")]
        answer = parts[1].strip()

        if queries and answer:
            json_data["queries"].append({"queries": queries, "answer": answer})
            save_data()
            print("Информация успешно добавлена.")
        else:
            print("Неверный формат ввода.")
    else:
        print("Неверный формат ввода.")


def web_search():
    search_term = input("Введите слово для поиска: ")
    with DDGS() as ddgs:
        results = [r["body"] for r in ddgs.text(search_term, max_results=5)]
        print(results)
        json_data["queries"].append({"queries": [search_term], "answer": results})
        save_data()
        print(f"Результаты поиска сохранены для запроса: {search_term}")


if __name__ == "__main__":
    user_query = input("Введите запрос: ")

    if user_query.lower() == "добавить свою инфу":
        add_custom_data()
    elif user_query.lower() == "websearch":
        web_search()
    else:
        result = search_json(user_query)
        print(result)
