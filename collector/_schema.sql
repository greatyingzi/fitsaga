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

CREATE TABLE IF NOT EXISTS suits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  game TEXT NOT NULL,
  name TEXT NOT NULL,
  slug TEXT,
  source TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  UNIQUE(game, name)
);
CREATE TABLE IF NOT EXISTS suit_imgs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  suit_id INTEGER NOT NULL,
  img_url TEXT UNIQUE,
  kind TEXT,
  raw_name TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_suits_game ON suits(game);
CREATE INDEX IF NOT EXISTS idx_suit_imgs_suit ON suit_imgs(suit_id);
