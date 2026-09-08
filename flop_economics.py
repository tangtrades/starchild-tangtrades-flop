# FLOP Network Miner Economics Engine & Verification Suite
# Calibrated to Arthur Hayes / Flop Labs specs (intro.flop.network DRAFT) & Jeff Tang's quantitative models.

class FlopEconomics:
    def __init__(
        self,
        total_supply: float = 17_200_000_000,
        circulating_tge: float = 2_864_400_000,
        circulating_p1: float = 1_023_600_000,
        era0_block_reward: float = 96.0,
        miner_share_reward: float = 0.75, # 72 FLOP/block
        halving_days: float = 730.0,
        total_blocks_era0: float = 63_072_000,
        h100_sustained_gns: float = 453_900.0,
        h100_sustained_tokens_sec: float = 1_110.0, # gpt-oss-120b MXFP4
        default_cloud_h100_monthly: float = 2_153.0,
        miner_share_fees: float = 0.85,
        fee_output_1m: float = 0.20,
        fee_input_1m: float = 0.04,
        base_network_h100_eq: float = 1200.0,
        # Flop Labs calibrated Era-0 accumulated block FLOP per 1/1,200 miner share
        calibrated_miner_era0_flop: float = 2_644_156.0,
        session_to_block_ratio: float = 0.057917
    ):
        self.total_supply = total_supply
        self.circulating_tge = circulating_tge
        self.circulating_p1 = circulating_p1
        self.era0_block_reward = era0_block_reward
        self.miner_reward_per_block = era0_block_reward * miner_share_reward
        self.halving_days = halving_days
        self.total_blocks_era0 = total_blocks_era0
        self.h100_sustained_gns = h100_sustained_gns
        self.h100_sustained_tokens_sec = h100_sustained_tokens_sec
        self.default_cloud_h100_monthly = default_cloud_h100_monthly
        self.miner_share_fees = miner_share_fees
        self.fee_output_1m = fee_output_1m
        self.fee_input_1m = fee_input_1m
        self.base_network_h100_eq = base_network_h100_eq
        self.calibrated_miner_era0_flop = calibrated_miner_era0_flop
        self.session_to_block_ratio = session_to_block_ratio

    def compute_scenario(self, fdv_usd: float, network_h100_eq: float = 1200.0, monthly_gpu_cost: float = 2153.0):
        """
        Computes 730-day Era-0 miner economics for 1 H100-equivalent.
        """
        token_price = fdv_usd / self.total_supply
        
        # Miner share scales inversely with network size
        miner_share_scaling = self.base_network_h100_eq / network_h100_eq
        miner_block_flop = self.calibrated_miner_era0_flop * miner_share_scaling
        block_reward_usd = miner_block_flop * token_price
        
        session_rev_usd = block_reward_usd * self.session_to_block_ratio
        gross_rev_usd = block_reward_usd + session_rev_usd
        
        # Fixed 730d capacity cost (calibrated to $52,390 for $2,153/mo)
        total_cost_usd = monthly_gpu_cost * (52390.0 / 2153.0)
        
        net_profit_usd = gross_rev_usd - total_cost_usd
        roi_pct = (net_profit_usd / total_cost_usd) * 100.0
        
        return {
            "fdv_usd": fdv_usd,
            "token_price_usd": token_price,
            "network_h100_eq": network_h100_eq,
            "monthly_gpu_cost": monthly_gpu_cost,
            "block_reward_flop": miner_block_flop,
            "block_reward_usd": block_reward_usd,
            "session_rev_usd": session_rev_usd,
            "gross_rev_usd": gross_rev_usd,
            "total_cost_usd": total_cost_usd,
            "net_profit_usd": net_profit_usd,
            "roi_pct": roi_pct
        }

    def breakeven_fdv(self, network_h100_eq: float = 1200.0, monthly_gpu_cost: float = 2153.0) -> float:
        """
        Solves for the exact FDV where Net Profit == 0 over 730 days.
        """
        total_cost_usd = monthly_gpu_cost * (52390.0 / 2153.0)
        miner_share_scaling = self.base_network_h100_eq / network_h100_eq
        miner_block_flop = self.calibrated_miner_era0_flop * miner_share_scaling
        
        # gross_rev_usd = miner_block_flop * (fdv / total_supply) * (1 + ratio) = total_cost_usd
        multiplier = miner_block_flop * (1.0 + self.session_to_block_ratio) / self.total_supply
        breakeven_fdv_usd = total_cost_usd / multiplier
        return breakeven_fdv_usd
