import unittest
from daa.greedy_algos import job_sequencing_with_deadlines

class TestJobSequencing(unittest.TestCase):
    def test_standard_case(self):
        # Jobs: (id, deadline, profit)
        jobs = [
            {'id': 'a', 'deadline': 2, 'profit': 100},
            {'id': 'b', 'deadline': 1, 'profit': 19},
            {'id': 'c', 'deadline': 2, 'profit': 27},
            {'id': 'd', 'deadline': 1, 'profit': 25},
            {'id': 'e', 'deadline': 3, 'profit': 15}
        ]
        # Expected: 
        # Sort profits: a(100), c(27), d(25), b(19), e(15)
        # 1. a(100, d=2) -> slot 1 (time 1-2)
        # 2. c(27, d=2) -> slot 0 (time 0-1)
        # 3. d(25, d=1) -> reject (slot 0 full)
        # 4. b(19, d=1) -> reject (slot 0 full)
        # 5. e(15, d=3) -> slot 2 (time 2-3)
        # Sequence: c, a, e
        
        sequence, total_profit = job_sequencing_with_deadlines(jobs)
        self.assertIn('a', sequence)
        self.assertIn('c', sequence)
        self.assertIn('e', sequence)
        self.assertEqual(len(sequence), 3)
        self.assertEqual(total_profit, 142)

    def test_impossible_deadlines(self):
        jobs = [
            {'id': 'a', 'deadline': 1, 'profit': 100},
            {'id': 'b', 'deadline': 1, 'profit': 200}
        ]
        # b takes slot 0. a rejected.
        sequence, total_profit = job_sequencing_with_deadlines(jobs)
        self.assertEqual(sequence, ['b'])
        self.assertEqual(total_profit, 200)

if __name__ == '__main__':
    unittest.main()
