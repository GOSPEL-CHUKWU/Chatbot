import json
from difflib import get_close_matches


def load_knowledge_base(filepath: str) -> dict:
    with open(filepath, 'r') as file:
        return json.load(file)


def update_knowledge_base(filepath: str, update: dict) -> None:
    with open(filepath, 'w') as file:
        json.dump(update, file, indent=2)


def find_best_matches(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, cutoff=0.6)
    return matches[0] if matches else None


def grab_answer(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base['questions']:
        if q['question'] == question:
            return q['answer']


def chatbot():
    knowledge_base = load_knowledge_base('knowledge_base.json')

    while True:
        user_input = input('You: ')

        if (user_input.lower() == 'quit'):
            break

        best_match = find_best_matches(
            user_input, [q['question'] for q in knowledge_base['questions']])

        if (best_match):
            answer = grab_answer(best_match, knowledge_base)
            print(f'Bot: {answer}')

        else:
            print(f'Bot: Sorry, I don\'t know the answer. Can you teach me?')
            user_skip = input('You: Type the answer or "skip" to skip: ')
            if (user_skip.lower() != 'skip'):
                knowledge_base['questions'].append(
                    {'question':  user_input, 'answer': user_skip})
                update_knowledge_base(
                    'knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learnt a new response')


if __name__ == '__main__':
    chatbot()
