import unittest
from flop_economics import FlopEconomics

class TestFlopEconomics(unittest.TestCase):
    def setUp(self):
        self.econ = FlopEconomics()

    def test_base_100m_fdv(self):
        res = self.econ.compute_scenario(fdv_usd=100_000_000, network_h100_eq=1200, monthly_gpu_cost=2153.0)
        self.assertAlmostEqual(res["token_price_usd"], 0.005814, places=5)
        self.assertAlmostEqual(res["net_profit_usd"], -36126, delta=100)
        self.assertAlmostEqual(res["roi_pct"], -68.96, delta=0.5)

    def test_breakeven_fdv(self):
        be_fdv = self.econ.breakeven_fdv(network_h100_eq=1200, monthly_gpu_cost=2153.0)
        self.assertAlmostEqual(be_fdv / 1e6, 322.0, delta=2.0)

    def test_bull_500m_fdv(self):
        res = self.econ.compute_scenario(fdv_usd=500_000_000, network_h100_eq=1200, monthly_gpu_cost=2153.0)
        self.assertAlmostEqual(res["net_profit_usd"], 28928, delta=150)
        self.assertAlmostEqual(res["roi_pct"], 55.2, delta=0.5)

if __name__ == "__main__":
    unittest.main()
