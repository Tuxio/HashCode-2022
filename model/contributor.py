class Contributor:
  def __init__(self, name, skills):
    self.name = name
    self.skills = skills
    self.available_at = 0

  def __repr__(self):
    return f"""Name: {self.name}, skills: {self.skills}"""