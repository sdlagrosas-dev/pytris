class DifficultyProfile:

    def __init__(self, name: str, difficulty_start_score: int, max_speed_score: int):
        """
        Initializes the DifficultyProfile with a name, difficulty start score, and maximum speed score.
        """
        self.name = name
        self.difficulty_start_score = difficulty_start_score
        self.max_speed_score = max_speed_score

    def __repr__(self):
        return f"DifficultyProfile(name={self.name}, difficulty_start_score={self.difficulty_start_score}, max_speed_score={self.max_speed_score})"


BEGINNER = DifficultyProfile("NOVICE", 4500, 40500)
INTERMEDIATE = DifficultyProfile("MEDIUM", 2500, 20500)
EXPERT = DifficultyProfile("MAKE 'EM RAIN", 800, 16000)
