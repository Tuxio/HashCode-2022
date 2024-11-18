class Project:
  def __init__(self, name, days, score, best_before, roles):
    self.name = name
    self.days = days
    self.score = score
    self.best_before = best_before
    self.roles = roles
    self.archived = False

  def __repr__(self):
    return f"""Name: {self.name}, days: {self.days}, score: {self.score}, best before: {self.best_before}, roles: {self.roles}"""