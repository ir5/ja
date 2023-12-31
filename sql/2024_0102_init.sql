CREATE TABLE aoj_acceptances (
  aoj_userid  VARCHAR(64) NOT NULL,
  problem_id  INTEGER NOT NULL,
  PRIMARY KEY (aoj_userid, problem_id)
);
CREATE INDEX ON aoj_acceptances (aoj_userid);
CREATE INDEX ON aoj_acceptances (problem_id);

CREATE TABLE problems (
  id        INTEGER NOT NULL,
  name      VARCHAR(255) NOT NULL,
  lang      INTEGER NOT NULL,
  plevel    INTEGER NOT NULL,
  org       VARCHAR(64) NOT NULL,
  used_in   VARCHAR(64) NOT NULL,
  slot      VARCHAR(64) NOT NULL,
  meta      TEXT NOT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX ON problems (id);

CREATE TABLE user_points (
  aoj_userid        VARCHAR(64) NOT NULL,
  total             INTEGER NOT NULL,
  counts_per_levels VARCHAR(255) NOT NULL,
  PRIMARY KEY (aoj_userid)
);
CREATE INDEX ON user_points (aoj_userid);
CREATE INDEX ON user_points (total DESC);

CREATE TABLE likes (
  github_id   BIGINT NOT NULL,
  problem_id  INTEGER NOT NULL,
  weight      INTEGER NOT NULL DEFAULT 1,
  PRIMARY KEY (github_id)
);
CREATE INDEX ON likes (problem_id);
