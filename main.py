from read_inputs import parse_input_file

if __name__ == '__main__':
    file_path = 'input_data/b_better_start_small.in.txt'
    contributors, projects = parse_input_file(file_path)

    print("Contributors:")
    for contributor in contributors:
        print(contributor)

    print("\nProjects:")
    for project in projects:
        print(project)
