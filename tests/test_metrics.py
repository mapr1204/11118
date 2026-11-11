import unittest
from analysis.calculate_metrics import metrics
from acquisition.mcc128_acquisition import engineering_units

class TestReferenceImplementation(unittest.TestCase):
    def test_metrics(self):
        m = metrics([1,2,3], [2,2,4])
        self.assertAlmostEqual(m['MAE'], 2/3)
        self.assertAlmostEqual(m['bias'], 2/3)
        self.assertAlmostEqual(m['RMSE'], (2/3)**.5)
    def test_scaling(self):
        c = dict(vmin=1,vmax=5,xmin=0,xmax=6,offset=0,gain=1)
        self.assertAlmostEqual(engineering_units(3,c),3)

if __name__ == '__main__':
    unittest.main()
