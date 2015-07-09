"""Test suite for fibermodes.simulator module"""

import unittest

from fibermodes import FiberFactory, Mode, ModeFamily
from fibermodes.simulator import Simulator


class TestSimulator(unittest.TestCase):

    """Test suite for Simulator class"""

    @property
    def Simulator(self):
        return Simulator

    def testUninitializedSimulator(self):
        sim = self.Simulator()
        with self.assertRaises(ValueError):
            sim.fibers

        with self.assertRaises(ValueError):
            sim.wavelengths

    def testConstructor(self):
        sim = self.Simulator('tests/fiber/smf28.fiber', 1550e-9)
        self.assertEqual(len(sim.wavelengths), 1)
        self.assertEqual(len(sim.fibers), 1)
        self.assertTrue(sim.initialized)
        self.assertTrue(sim._fsims is not None)

    def testSetWavelengths(self):
        sim = self.Simulator()
        sim.set_wavelengths(1550e-9)
        self.assertEqual(len(sim.wavelengths), 1)
        self.assertEqual(sim.wavelengths[0], 1550e-9)

        sim.set_wavelengths([1550e-9, 1560e-9])
        self.assertEqual(len(sim.wavelengths), 2)

        sim.set_wavelengths({'start': 1550e-9,
                             'end': 1580e-9,
                             'num': 4})
        self.assertEqual(len(sim.wavelengths), 4)

        with self.assertRaises(ValueError):
            sim.fibers
        self.assertFalse(sim.initialized)
        self.assertTrue(sim._fsims is None)

    def testSetFactory(self):
        sim = self.Simulator()
        sim.set_factory('tests/fiber/rcfs.fiber')
        self.assertEqual(len(sim.fibers), 5)

        f = FiberFactory()
        f.addLayer(radius=[4e-6, 5e-6, 6e-6], index=1.449)
        f.addLayer(index=1.444)
        sim.set_factory(f)
        self.assertEqual(len(sim.fibers), 3)

        with self.assertRaises(ValueError):
            sim.wavelengths
        self.assertFalse(sim.initialized)
        self.assertTrue(sim._fsims is None)

    def testModesSMF(self):
        sim = self.Simulator('tests/fiber/smf28.fiber', 1550e-9, scalar=True)
        modes = list(sim.modes())
        self.assertEqual(len(modes), 1)
        modesf1 = modes[0]
        self.assertEqual(len(modesf1), 1)
        modeswl1 = modesf1[0]
        self.assertEqual(len(modeswl1), 2)
        self.assertTrue(Mode(ModeFamily.HE, 1, 1) in modeswl1)
        self.assertTrue(Mode(ModeFamily.LP, 0, 1) in modeswl1)

    def testModesRCF(self):
        sim = self.Simulator('tests/fiber/rcfs.fiber', 1550e-9)
        modes = list(sim.modes())
        self.assertEqual(len(modes), 5)
        for fmodes in modes:
            self.assertEqual(len(fmodes), 1)

    def testCutoff(self):
        sim = self.Simulator('tests/fiber/rcfs.fiber', 1550e-9)
        co = list(sim.cutoff())
        self.assertEqual(len(co), 5)
        for fco in co:
            self.assertEqual(len(fco), 1)
            self.assertEqual(fco[0][Mode('HE', 1, 1)], 0)

    def testNeff(self):
        sim = self.Simulator('tests/fiber/smf28.fiber', 1550e-9, delta=1e-4)
        neff = list(sim.neff())
        self.assertEqual(len(neff), 1)
        self.assertAlmostEqual(neff[0][0][Mode('HE', 1, 1)], 1.446386514937099)

if __name__ == "__main__":
    import os
    os.chdir("../..")
    unittest.main()