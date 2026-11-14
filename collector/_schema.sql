CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  src_id TEXT,
  img_url TEXT UNIQUE,
  origin_url TEXT,
  author TEXT,
  license TEXT,
  w INTEGER, h INTEGER,
  tags TEXT,
  aigc_label INTEGER,
  raw TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_items_source ON items(source);
CREATE INDEX IF NOT EXISTS idx_items_tags ON items(tags);
