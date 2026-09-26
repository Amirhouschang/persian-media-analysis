-- 05_check_cleaning.sql – Checks after 04_clean_text.py
-- Run in DBeaver (database iran_media_2026).

-- 1. Must not occur any more (first two values must be 0)
--    text_lost = posts with Persian text that are empty after cleaning (should only be pure advertising lines)
SELECT
  COUNT(*) FILTER (WHERE text_clean ~ '[يكة]')                     AS arabic_letters,
  COUNT(*) FILTER (WHERE text_clean ~* 'https?://|t\.me/|@\w')     AS links_mentions,
  COUNT(*) FILTER (WHERE text ~ '[آ-ی]{2,}' AND word_count = 0)    AS text_lost
FROM posts;

-- 1b. Show these posts
SELECT post_id, channel_id, text, text_clean
FROM posts
WHERE text_clean ~* 'https?://|t\.me/|@\w'
   OR (text ~ '[آ-ی]{2,}' AND word_count = 0);

-- 2. Posts with the most removed words: only advertising, links and @mentions may be missing
SELECT channel_id, post_id,
       regexp_count(text, '[آ-ی‌]+') - word_count AS lost_words,
       text, text_clean
FROM posts
ORDER BY lost_words DESC
LIMIT 20;

-- 3. Random sample: compare original and cleaned text by reading
SELECT text, text_clean
FROM posts
WHERE word_count > 0
ORDER BY random()
LIMIT 20;
