import unittest
from tasks import TASKS, grader

class TestGrader(unittest.TestCase):
    def test_scores_strictly_between_zero_and_one(self):
        task = TASKS[0] # easy_password_reset
        
        # Test 1: Perfect score (should be capped at 0.99)
        perfect_state = {
            "route": task.expected_route
        }
        score1 = grader(task, perfect_state)
        self.assertTrue(0.0 < score1 < 1.0, f"Perfect score {score1} is not strictly between 0 and 1")
        self.assertEqual(score1, 0.99)
        
        # Test 2: Zero score (should be floored at 0.01)
        poor_state = {
            "route": "WRONG_ROUTE"
        }
        score2 = grader(task, poor_state)
        self.assertTrue(0.0 < score2 < 1.0, f"Zero score {score2} is not strictly between 0 and 1")
        self.assertEqual(score2, 0.01)

    def test_medium_task_partial_score(self):
        task = TASKS[1] # medium_hardware_issue
        
        # Test partial state (route is right, but missing info)
        partial_state = {
            "route": task.expected_route,
            "collected_info": [] 
        }
        score = grader(task, partial_state)
        self.assertTrue(0.0 < score < 1.0, f"Partial score {score} is not strictly between 0 and 1")

if __name__ == "__main__":
    unittest.main()
