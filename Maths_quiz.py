# quiz.py

import pathlib
import random
from string import ascii_lowercase
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

NUM_QUESTIONS_PER_QUIZ = 10
QUESTIONS_PATH = pathlib.Path(__file__).parent / "Maths_questions.toml"

def run_quiz():
    questions = prepare_questions(
        QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ
    )

    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\nQuestion {num} :")
        num_correct += ask_question(question)
    if num_correct == len(questions):
        print("\n Félicitations ! Vous avez tout juste ! \n Maintenant fais des partiels des années précédentes !")
    print(f"\nVous avez {num_correct} réponses correctes sur {num} questions.")

def prepare_questions(path, num_questions):
    topic_info = tomllib.loads(path.read_text(encoding='utf-8'))
    topics = {
        topic["label"]: topic["questions"] for topic in topic_info.values()
    }
    topic_label = get_answers(
        question="Sur quel sujet voulez-vous être interrogé ",
        alternatives=sorted(topics),
    )[0]

    questions = topics[topic_label]
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)

def ask_question(question):
    correct_answers = question["answers"]
    alternatives = question["answers"] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answers = get_answers(
        question=question["question"],
        alternatives=ordered_alternatives,
        num_choices=len(correct_answers),
        hint=question.get("hint"),
    )
    if correct := (set(answers) == set(correct_answers)):
        print("⭐ Correct ⭐")
    else:
        is_or_are = "la réponse est" if len(correct_answers) == 1 else "les réponses sont"
        print("\n- ".join([f"Non, {is_or_are} :"] + correct_answers))

    if "explanation" in question:
        print(f"\nExplication :\n{question['explanation']}")

    return 1 if correct else 0

def get_answers(question, alternatives, num_choices=1, hint=None):
    print(f"{question}?")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    if hint:
        labeled_alternatives[""] = "Hint"

    for label, alternative in labeled_alternatives.items():
        print(f"  {label}) {alternative}")

    while True:
        answer = input(f"\nChoix  ")
        answers = set(answer.replace(",", " ").split())

        # Handle hints
        if hint and "?" in answers:
            print(f"\nHINT: {hint}")
            continue

        # Handle invalid answers
        if len(answers) != num_choices:
            plural_s = "" if num_choices == 1 else "s, separated by comma"
            print(f"Please answer {num_choices} alternative{plural_s}")
            continue

        if any(
            (invalid := answer) not in labeled_alternatives
            for answer in answers
        ):
            print(
                f"{invalid!r} n'est pas un choix valide. "
                f"S'il vous plaît, utilisez {', '.join(labeled_alternatives)}"
            )
            continue

        return [labeled_alternatives[answer] for answer in answers]

if __name__ == "__main__":
    run_quiz()
