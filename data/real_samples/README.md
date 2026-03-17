# Real Sample Data

Drop the first real verification sample here:

- `xauusd_4h.csv`

Use the schema:

```csv
symbol,timestamp,timeframe,open,high,low,close
XAUUSD,2026-03-16T00:00:00Z,4H,2990.0,3001.0,2988.5,2998.0
```

Rules:

- only closed candles
- timestamps sorted ascending
- timestamps normalized to UTC if possible
- one symbol only for the first verification pass
- one timeframe only for the first verification pass

Do not commit large raw exports by default. Start with a small, reviewable
sample of 20 to 100 rows.
