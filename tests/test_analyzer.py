import unittest
from analyzer import find_skills, analyze_resume

class AnalyzerTests(unittest.TestCase):
    def test_skill_detection(self):
        text = "Built dashboards using Python, SQL, Pandas and Power BI."
        found = find_skills(text)
        self.assertIn("python", found)
        self.assertIn("sql", found)
        self.assertIn("pandas", found)
        self.assertIn("power bi", found)

    def test_whole_term_matching(self):
        found = find_skills("I enjoy python programming.")
        self.assertIn("python", found)
        self.assertNotIn("java", found)

    def test_analysis_output(self):
        resume = "Python SQL Pandas Excel. Developed data analysis projects in 2025."
        job = "Python SQL Power BI Excel data analysis communication."
        result = analyze_resume(resume, job)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertIn("python", result["matched_skills"])
        self.assertIn("power bi", result["missing_skills"])
        self.assertIsInstance(result["suggestions"], list)

if __name__ == "__main__":
    unittest.main()
