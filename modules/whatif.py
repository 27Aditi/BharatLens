

def simulate(
    base_nifty: float,
    rbi_rate_delta: float,     # change in % (e.g. +0.5 means hike by 50 bps)
    crude_delta: float,        # change in USD/barrel
    usd_inr_delta: float,      # change in INR per USD
    fdi_delta: float,          # change in $B
) -> dict:
    
    rate_impact  = -(rbi_rate_delta / 0.25) * 1.2       # per 25 bps
    crude_impact = -(crude_delta    / 5.0)  * 0.4        # per $5
    fx_impact    = -(usd_inr_delta)         * 0.3        # per ₹1
    fdi_impact   =  (fdi_delta)             * 0.6        # per $1B

    total_pct    = rate_impact + crude_impact + fx_impact + fdi_impact
    new_nifty    = round(base_nifty * (1 + total_pct / 100), 2)

    sectors = {
        "Banking & Finance": round(-rbi_rate_delta * 2.5, 2),
        "IT & Tech":         round( usd_inr_delta  * 0.8, 2),   # IT benefits from weak INR
        "Oil & Energy":      round(-crude_delta     * 0.6, 2),
        "Auto":              round(-crude_delta     * 0.4 - rbi_rate_delta * 1.5, 2),
        "FMCG":              round(-crude_delta     * 0.2, 2),
        "Pharma":            round( usd_inr_delta  * 0.5, 2),
    }

    reasons = []
    if rbi_rate_delta != 0:
        direction = "hike" if rbi_rate_delta > 0 else "cut"
        reasons.append(
            f"RBI rate {direction} of {abs(rbi_rate_delta):.2f}% → borrowing costs "
            f"{'rise' if rbi_rate_delta > 0 else 'fall'}, "
            f"market {'contracts' if rbi_rate_delta > 0 else 'expands'} ({rate_impact:+.2f}%)"
        )
    if crude_delta != 0:
        reasons.append(
            f"Crude {'up' if crude_delta > 0 else 'down'} ${abs(crude_delta):.1f}/barrel → "
            f"import bill {'increases' if crude_delta > 0 else 'decreases'} ({crude_impact:+.2f}%)"
        )
    if usd_inr_delta != 0:
        reasons.append(
            f"INR {'weakens' if usd_inr_delta > 0 else 'strengthens'} by ₹{abs(usd_inr_delta):.1f} → "
            f"imported inflation {'rises' if usd_inr_delta > 0 else 'falls'} ({fx_impact:+.2f}%)"
        )
    if fdi_delta != 0:
        reasons.append(
            f"FDI {'inflow' if fdi_delta > 0 else 'outflow'} of ${abs(fdi_delta):.1f}B → "
            f"capital {'enters' if fdi_delta > 0 else 'exits'} market ({fdi_impact:+.2f}%)"
        )

    return {
        "base_nifty":    base_nifty,
        "new_nifty":     new_nifty,
        "total_change":  round(total_pct, 2),
        "sector_impact": sectors,
        "reasons":       reasons,
    }
