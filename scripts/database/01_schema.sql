-- 01_schema.sql – structure of the database iran_media_2026
-- ==========================================================
-- Executed by 02_load_database.py. Existing tables are dropped and rebuilt,
-- so the load can be repeated at any time with the same result.
--
-- source_groups 1 ──< channels 1 ──< posts >── 1 dates >── 1 phases

DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS channels;
DROP TABLE IF EXISTS source_groups;
DROP TABLE IF EXISTS dates;
DROP TABLE IF EXISTS phases;

-- One row per source group
CREATE TABLE source_groups (
    group_id      SMALLINT PRIMARY KEY,
    name          TEXT NOT NULL UNIQUE,         -- 'state', 'irgc_affiliated', 'reformist'
    description   TEXT
);

-- One row per Telegram channel
CREATE TABLE channels (
    channel_id    SMALLINT PRIMARY KEY,
    username      TEXT NOT NULL UNIQUE,         -- Telegram user name, e.g. 'Tasnimnews'
    name          TEXT NOT NULL,                -- readable name, e.g. 'Tasnim News'
    group_id      SMALLINT NOT NULL REFERENCES source_groups(group_id),
    channel_url   TEXT NOT NULL,                -- e.g. https://t.me/Tasnimnews
    description   TEXT                          -- neutral description (same as in the AI codebook)
);

-- Phases of the observation period (boundaries set by the author, see 02_load_database.py)
CREATE TABLE phases (
    phase_id      SMALLINT PRIMARY KEY,
    name          TEXT NOT NULL UNIQUE,
    start_date    DATE NOT NULL,
    end_date      DATE NOT NULL,
    description   TEXT
);

-- One row per calendar day (date dimension), 1 Jan – 31 Aug 2026
CREATE TABLE dates (
    date_key      INTEGER PRIMARY KEY,          -- YYYYMMDD, e.g. 20260228
    date          DATE NOT NULL UNIQUE,
    year          SMALLINT NOT NULL,
    month         SMALLINT NOT NULL,
    month_name    TEXT NOT NULL,
    iso_week      SMALLINT NOT NULL,
    week_start    DATE NOT NULL,                -- Monday of the week
    weekday       SMALLINT NOT NULL,            -- 1 = Monday ... 7 = Sunday
    weekday_name  TEXT NOT NULL,
    phase_id      SMALLINT NOT NULL REFERENCES phases(phase_id)
);

-- One row per post
CREATE TABLE posts (
    channel_id      SMALLINT    NOT NULL REFERENCES channels(channel_id),
    post_id         BIGINT      NOT NULL,       -- post number within the channel
    date_key        INTEGER     NOT NULL REFERENCES dates(date_key),   -- day of publication (UTC)
    published_at    TIMESTAMPTZ NOT NULL,       -- exact publication time (UTC)
    text            TEXT,                       -- post text (Persian), empty for images/videos without caption
    views           BIGINT,
    forwards        BIGINT,
    forwarded_from  TEXT,                       -- origin, if the post itself was forwarded
    post_url        TEXT NOT NULL,              -- e.g. https://t.me/Tasnimnews/424439
    -- filled by 04_clean_text.py (run it again after every reload):
    text_clean      TEXT,                       -- normalised text without links, signatures, emojis
    tokens          TEXT,                       -- content words separated by spaces (stop words removed)
    word_count      INTEGER,                    -- number of words in text_clean
    PRIMARY KEY (channel_id, post_id)
);

CREATE INDEX idx_posts_published_at ON posts (published_at);
CREATE INDEX idx_posts_date_key ON posts (date_key);
