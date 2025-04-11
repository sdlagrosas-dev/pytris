class DifficultyProfile:
    """
    Attributes
    ----------
    - name: str
        The name of the difficulty profile.
    - difficulty_start_score: int
        The starting score when the difficulty increases.
    - max_speed_score: int
        The maximum score for speed.
    """

    def __init__(self, name: str, difficulty_start_score: int, max_speed_score: int):
        """
        Initializes the DifficultyProfile with a name, difficulty start score, and maximum speed score.

        Parameters
        ----------
        - name: str
            The name of the difficulty profile.
        - difficulty_start_score: int
            The starting score when the difficulty increases.
        - max_speed_score: int
            The maximum score for speed.
        """
        self.name = name
        self.difficulty_start_score = difficulty_start_score
        self.max_speed_score = max_speed_score

    def __repr__(self):
        return f"DifficultyProfile(name={self.name}, difficulty_start_score={self.difficulty_start_score}, max_speed_score={self.max_speed_score})"


BEGINNER = DifficultyProfile("NOVICE", 5000, 45000)
INTERMEDIATE = DifficultyProfile("MEDIUM", 2500, 22500)
EXPERT = DifficultyProfile("MAKE 'EM RAIN", 1000, 8000)
