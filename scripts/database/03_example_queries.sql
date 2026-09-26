-- 03_example_queries.sql – first queries to explore the data (e.g. in DBeaver)
-- ============================================================================

-- All times in UTC (same as the Python analysis)
SET TIME ZONE 'UTC';

-- Posts per channel
SELECT c.name AS channel, g.name AS source_group, COUNT(*) AS posts
FROM posts p
JOIN channels c ON c.channel_id = p.channel_id
JOIN source_groups g ON g.group_id = c.group_id
GROUP BY c.name, g.name
ORDER BY posts DESC;

-- Posts of one channel, newest first, with link
SELECT p.published_at, p.views, p.post_url, LEFT(p.text, 120) AS text_start
FROM posts p
JOIN channels c ON c.channel_id = p.channel_id
WHERE c.username = 'Tasnimnews'
ORDER BY p.published_at DESC
LIMIT 50;

-- Posts per week and source group
SELECT date_trunc('week', p.published_at) AS week, g.name AS source_group, COUNT(*) AS posts
FROM posts p
JOIN channels c ON c.channel_id = p.channel_id
JOIN source_groups g ON g.group_id = c.group_id
GROUP BY week, g.name
ORDER BY week, g.name;

-- Average views and forwards per post and channel (posts with a view count only)
SELECT c.name AS channel, ROUND(AVG(p.views)) AS avg_views, ROUND(AVG(p.forwards)) AS avg_forwards
FROM posts p
JOIN channels c ON c.channel_id = p.channel_id
WHERE p.views IS NOT NULL
GROUP BY c.name
ORDER BY avg_views DESC;

-- Days without posts per channel (gaps)
SELECT c.name AS channel, d::date AS day_without_posts
FROM channels c
CROSS JOIN generate_series('2026-01-01'::date, '2026-08-31'::date, interval '1 day') AS d
WHERE NOT EXISTS (
    SELECT 1 FROM posts p
    WHERE p.channel_id = c.channel_id AND p.published_at::date = d::date
)
ORDER BY c.name, day_without_posts;

-- Posts in the week before and after the start of the war (28 Feb 2026)
SELECT c.name AS channel,
       COUNT(*) FILTER (WHERE p.published_at >= '2026-02-21' AND p.published_at < '2026-02-28') AS week_before,
       COUNT(*) FILTER (WHERE p.published_at >= '2026-02-28' AND p.published_at < '2026-03-07') AS week_after
FROM posts p
JOIN channels c ON c.channel_id = p.channel_id
GROUP BY c.name
ORDER BY c.name;

-- Posts per phase and source group, per day (phases have different lengths)
SELECT ph.name AS phase, g.name AS source_group,
       COUNT(*) AS posts,
       ROUND(COUNT(*)::numeric / COUNT(DISTINCT d.date_key), 1) AS posts_per_day
FROM posts p
JOIN dates d ON d.date_key = p.date_key
JOIN phases ph ON ph.phase_id = d.phase_id
JOIN channels c ON c.channel_id = p.channel_id
JOIN source_groups g ON g.group_id = c.group_id
GROUP BY ph.phase_id, ph.name, g.name
ORDER BY ph.phase_id, g.name;

-- Posts per weekday (are there fewer posts on Fridays?)
SELECT d.weekday, d.weekday_name, COUNT(*) AS posts
FROM posts p
JOIN dates d ON d.date_key = p.date_key
GROUP BY d.weekday, d.weekday_name
ORDER BY d.weekday;
