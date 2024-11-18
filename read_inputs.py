from model.project import Project
from model.contributor import Contributor


def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    c_count, p_count = map(int, lines[0].strip().split())
    contributors = []
    projects = []
    index = 1

    # contributors
    for _ in range(c_count):
        name, n = lines[index].strip().split()
        n = int(n)

        index += 1
        skills = {}
        for __ in range(n):
            skill_name, skill_level = lines[index].strip().split()
            skills[skill_name] = int(skill_level)
            index += 1
        contributors.append(Contributor(name, skills))

    # projects
    for _ in range(p_count):
        name, days, score, best_before, roles = lines[index].strip().split()
        days, score, best_before, roles = map(int, [days, score, best_before, roles])
        index += 1
        conv_roles = []
        for __ in range(roles):
            role_skill, role_level = lines[index].strip().split()
            conv_roles.append({'skill': role_skill, 'level': int(role_level)})
            index += 1
        projects.append(Project(name, days, score, best_before, conv_roles))

    return contributors, projects
