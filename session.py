import base64
import json
import os
import random
import shutil
import urllib.request

from jinja2 import Environment
from names_generator import generate_name

TEST_BASE_PATH = "/tmp/k8s-game-rule-main/tests"


def get_tasks(game: str):
    get_tests()
    folder = f"{TEST_BASE_PATH}/{game}/"
    tasks = []
    for file in sorted(os.listdir(folder)):
        if os.path.isdir(os.path.join(folder, file)) and "99_test_template" not in file:
            tasks.append(file)
    return tasks


def get_tests():
    if not os.path.exists("/tmp/k8s-game-rule-main.zip"):
        url = "https://github.com/practical-bootcamp/k8s-game-rule/archive/refs/heads/main.zip"
        urllib.request.urlretrieve(url, "/tmp/k8s-game-rule-main.zip")
        shutil.unpack_archive("/tmp/k8s-game-rule-main.zip", "/tmp/")


def get_session_template(game: str, task: str):
    get_tests()
    session = {}
    game_session_file = f"{TEST_BASE_PATH}/{game}/session.json"
    task_session_file = f"{TEST_BASE_PATH}/{game}/{task}/session.json"
    if os.path.exists(game_session_file):
        with open(game_session_file, "r", encoding="utf-8") as file:
            game_session = json.load(file)
            session.update(game_session)
    if os.path.exists(task_session_file):
        with open(task_session_file, "r", encoding="utf-8") as file:
            task_session = json.load(file)
            session.update(task_session)

    return session


def get_instruction(game: str, task: str, session: dict):
    get_tests()
    instructions_file = f"{TEST_BASE_PATH}/{game}/{task}/instruction.md"

    if os.path.exists(instructions_file):
        with open(instructions_file, "r", encoding="utf-8") as file:
            instruction = file.read()
        return render(instruction, session)
    return None


def random_name(seed: str = "") -> str:
    return generate_name(style="underscore", seed=seed).replace("_", "")


def random_number(from_number: int, to_number: int, seed: str = "") -> str:
    random.seed(seed)
    return str(random.randint(from_number, to_number))


def base64_encode(value: str) -> str:
    return base64.b64encode(value.encode()).decode()


def render(template, func_dict):
    env = Environment()
    jinja_template = env.from_string(template)
    jinja_template.globals.update(func_dict)
    template_string = jinja_template.render()
    return template_string


def generate_session(email: str, game: str, task: str) -> dict:
    session = get_session_template(game, task)

    student_id = email.split("@")[0]
    func_dict = {
        "student_id": lambda: student_id,
        "random_name": lambda: random_name(student_id),
        "random_number": lambda f, to: random_number(f, to, student_id),
        "base64_encode": base64_encode,
    }

    session = {
        k: render(v, func_dict) if isinstance(v, str) else v for k, v in session.items()
    }

    return session
