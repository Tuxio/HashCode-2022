from read_inputs import parse_input_file


def assign_contributors_to_projects(contributors, projects):
    # zuerst nach best_before, dann nach score sortieren
    projects.sort(key=lambda p: (p.best_before, -p.score))

    assignments = []
    score = 0
    project_start_time = 0
    i = 0
    while (any(p.archived == False for p in projects) and i < 100):
        i = i+ 1
        for project in projects:
            if project.archived:
                continue;

            roles_filled = []

            # Ueberpruefen, ob es Rollen gibt, die zu dem aktuellen Projekt passen
            for role in project.roles:
                skill = role['skill']
                level_required = role['level']
                candidate = None
                mentor_present = False
                for contributor in contributors:
                    # Ueberpruefen, ob ein contributor zu dem Startzeitpunkt verfuegbar ist (oder zu einem spaetern zeitpunkt bevor der score 0 erreicht)
                    # und der benoetigte Skill oder ein anderer contributer mit skill+1 zum anlernen verfuegbar ist
                    if contributor.available_at <= project_start_time or contributor.available_at <= project.best_before:
                        if contributor.skills.get(skill, 0) >= level_required:
                            candidate = contributor
                            break
                        elif contributor.skills.get(skill, 0) == level_required - 1:
                            mentor_present = any(
                                c.skills.get(skill, 0) >= level_required for c in contributors if c != contributor
                            )
                            if mentor_present:
                                # todo evtl hier auch den mentor als candidate angeben
                                candidate = contributor
                                break

                if candidate:
                    roles_filled.append(candidate)

                    project_start_time = max(project_start_time, candidate.available_at)

                    # Skill verbessern wenn ein contributer einen mentor besitzt
                    if candidate.skills.get(skill, 0) == level_required - 1:
                        candidate.skills[skill] = level_required
                    candidate.available_at = project_start_time + project.days
                    candidate.skills[skill] = candidate.skills[skill] + 1 # todo bei jedem richtig??
                else:
                    # Projekt skippen, wenn es keine Rolle gibt, die mit diesem Projekt besetzt werden kann
                    break
            else:
                # Nur wenn einem Projekt alle Rollen zugeordnet wurden, das Projekt hinzufuegen
                project.archived = True
                score_gained = max(0, project.score - (project_start_time + project.days - project.best_before)) \
                    if (project_start_time > project.best_before) else project.score
                score += score_gained
                assignments.append((project.name, [c.name for c in roles_filled], project_start_time, score_gained))

    return assignments, score


if __name__ == '__main__':
    file_path = 'input_data/a_an_example.in.txt'
    contributors, projects = parse_input_file(file_path)

    print("Contributors:")
    for contributor in contributors:
        print(contributor)

    print("\nProjects:")
    for project in projects:
        print(project)

    result, score = assign_contributors_to_projects(contributors, projects)

    print(len(result))
    for project_name, contributor_names, time_start, score_gained in result:
        print(project_name, time_start, score_gained)
        print(" ".join(contributor_names))
    print(score)

    print("Contributors mit neu erworbenen skills:")
    for contributor in contributors:
        print(contributor)
