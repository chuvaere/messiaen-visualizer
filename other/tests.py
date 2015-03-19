import unittest
import datetime

import matcher
import pickle

class TestMaxMspFunctions(unittest.TestCase):
    def test_bang(self):
        self.assertIsNotNone(matcher.bang)
    def test_clear(self):
        self.assertIsNotNone(matcher.clear)

class TestModeCharacteristics(unittest.TestCase):
    def test_all_modes(self):
        self.assertEqual(len(matcher.all_modes), 35)
    def test_color_modes(self):
        self.assertEqual(len(matcher.color_modes), 19)

class TestSimpleVectorCalc(unittest.TestCase):
    def setUp(self):
        self.buffer = matcher.NoteBuffer()
        for i in range(12, 24):
            self.buffer.add(i, 40, datetime.datetime.now())
    def test_simple_vector(self):
        self.assertEqual(len(self.buffer.buffer), 12)
        self.assertEqual(len(self.buffer.get_active()), 12)
        for i in matcher.simple_vector_calc(self.buffer).note_vector:
            self.assertTrue(i == 1)


  
class TestNoteSetOperations(unittest.TestCase):
    def setUp(self):
        self.set1 = matcher.NoteSet([0, 2, 4, 6, 8, 10])
        self.set2 = matcher.NoteSet([1, 3, 5, 7, 9, 11])
    def test_intersection(self):
        self.assertTrue(self.set1.intersection(self.set2).note_set == set([]))
    def test_union(self):
        self.assertTrue(
            len(self.set1.union(self.set2).note_vector) == 12)
    def test_difference(self):
        self.assertTrue(
            len(self.set1.union(self.set2).note_vector) == 12)
    def test_distance(self):
        self.assertTrue(
            self.set1.distance(self.set2) == pow(12, 0.5))
    def test_note_vector(self):
        nv1 = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        nv2 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        for i in range(12):
            self.assertTrue(self.set1.note_vector[i] == nv1[i])
        for i in range(12):
            self.assertTrue(self.set2.note_vector[i] == nv2[i])
    def test_nearest(self):
        self.assertIs(self.set1.nearest(matcher.all_modes), matcher.M1T1)
        self.assertIs(self.set2.nearest(matcher.all_modes), matcher.M1T2)

class TestNoteBufferOperations(unittest.TestCase):
    def setUp(self):
        file = open('/Users/n91p817/sample_buffer.pickle', 'r')
        self.buffer = pickle.load(file)
    def test_get_last_n(self):
        self.assertEqual(
            len(self.buffer.get_last_n(5)), 5)
    def test_get_last_nsec(self):
        pass
    def test_get_last_note(self):
        self.assertIsInstance(
            self.buffer.get_last_note(62), matcher.NoteEvent)
    def test_get_active(self):
        notes = self.buffer.get_active()
        self.assertEqual(
            len(notes), 8)
        for i in notes:
            self.assertIsInstance(i, matcher.NoteEvent)
            self.assertIsNone(i.end_time)
    def test_get_inactive(self):
        notes = self.buffer.get_inactive()
        for i in notes:
            self.assertIsInstance(i, matcher.NoteEvent)
            self.assertGreater(i.end_time, i.start_time)
    def test_get_all(self):
        notes = self.buffer.get_all()
        for i in notes:
            self.assertIsInstance(i, matcher.NoteEvent)
    def test_close_last(self):
        pass
    def test_get_heights(self):
        pass

if __name__ == '__main__':
    unittest.main()