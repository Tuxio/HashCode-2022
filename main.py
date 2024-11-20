from read_inputs import parse_input_file

# todo:
#  Not possessing a skill is equivalent to possessing a skill at level 0. So a contributor can work on a project and be assigned to a role with requirement C++ level 1 if they don’t know any C++, provided that somebody else on the team knows C++ at level 1 or higher.
def assign_contributors_to_projects(contributors, projects):
    # zuerst nach best_before, dann nach score sortieren
    projects.sort(key=lambda p: (p.best_before, -p.score))

    assignments = []
    score = 0
    days = set([0])
    while len(days) > 0:
        day = min(days)
        days.remove(day)
        print(f"Tag: {day} {days}")
        for project in projects:
            print(f"""project: {project.name}""")
            if project.archived:
                continue

            roles_filled = []
            mentor_list_to_role = []

            # Ueberpruefen, ob es Rollen gibt, die zu dem aktuellen Projekt passen
            for role in project.roles:
                skill = role['skill']
                level_required = role['level']
                candidate = None
                for contributor in contributors:
                    # Ueberpruefen, ob ein contributor zu dem Startzeitpunkt verfuegbar ist
                    # und der benoetigte Skill oder ein anderer contributer mit skill+1 zum anlernen verfuegbar ist
                    if contributor.available_at <= day:
                        if contributor.skills.get(skill, 0) >= level_required:
                            candidate = contributor
                            break
                        elif contributor.skills.get(skill, 0) == level_required - 1:
                            mentor_present = any(
                                c.skills.get(skill, 0) >= level_required for c in contributors if c != contributor
                            )
                            if mentor_present:
                                for mentor in contributors:
                                    if mentor.skills.get(skill, 0) >= level_required and mentor != contributor:
                                        mentor_list_to_role.append({mentor: mentor, skill: skill})
                                candidate = contributor
                            break

                if candidate:
                    roles_filled.append(candidate)
                else:
                    # Projekt skippen, wenn es keine Rolle gibt, die mit diesem Projekt besetzt werden kann
                    break
            else:
            # if len(roles_filled) > 0:
                # Nur wenn einem Projekt alle Rollen zugeordnet wurden, das Projekt hinzufuegen
                project.archived = True
                end_day = day + project.days
                score_gained = max(0, project.score - (day + project.days - project.best_before)) \
                    if (day > project.best_before) else project.score
                score += score_gained
                assignments.append((project.name, [c.name for c in roles_filled], day, end_day, score_gained))

                # Skill und available day fuer die candidates, die am Projekt teilnehmen anpassen
                for c in roles_filled:
                    for cs in c.skills:
                        # test = lambda (project.roles) : (project.roles['skill'])
                        skill_is_needed = any(
                            rs['skill'] == cs for rs in project.roles
                        )
                        if skill_is_needed:

                            is_mentor = False
                            # Skill verbessern
                            for ms in mentor_list_to_role:
                                if ms.mentor == c:
                                    is_mentor = True

                            for pr in project.roles:
                                if pr['skill'] == cs:
                                    if not is_mentor and c.skills[cs] <= pr['level']:
                                        c.skills[cs] = c.skills[cs] + 1
                                    c.available_at = day + project.days


                days.add(end_day)
        print(f"sdsad {days}")
    return assignments, score


if __name__ == '__main__':
    file_path = 'input_data/b_better_start_small.in.txt'
    contributors, projects = parse_input_file(file_path)

    print("Contributors:")
    for contributor in contributors:
        print(contributor)

    print("\nProjects:")
    for project in projects:
        print(project)

    result, score = assign_contributors_to_projects(contributors, projects)

    print(len(result))
    for project_name, contributor_names, time_start, end_day, score_gained in result:
        print(project_name, time_start, end_day, score_gained)
        print(" ".join(contributor_names))
    print(score)

    print("Contributors mit neu erworbenen skills:")
    for contributor in contributors:
        print(contributor)
