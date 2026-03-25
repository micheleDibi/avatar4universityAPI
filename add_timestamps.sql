-- Add created_at and updated_at columns with automatic management via triggers
-- - created_at: set automatically on INSERT via trigger, never changes
-- - updated_at: set automatically on INSERT and UPDATE via triggers
-- For existing rows, both are set to 2026-03-23T00:00:00

-- ============================================================
-- 1. Add columns with constant default for existing rows
-- ============================================================

ALTER TABLE modules ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE modules ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

ALTER TABLE lessons ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE lessons ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

ALTER TABLE sections ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE sections ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

ALTER TABLE slides ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE slides ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

ALTER TABLE quizzes ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE quizzes ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

ALTER TABLE quiz_questions ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE quiz_questions ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

ALTER TABLE quiz_options ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE quiz_options ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

ALTER TABLE open_questions ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE open_questions ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

ALTER TABLE text_books ADD COLUMN created_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';
ALTER TABLE text_books ADD COLUMN updated_at DATETIME NOT NULL DEFAULT '2026-03-23T00:00:00';

-- ============================================================
-- 2. Triggers: auto-set timestamps on INSERT and UPDATE
--    (overrides the constant default for new rows)
-- ============================================================

-- modules
CREATE TRIGGER trg_modules_insert
AFTER INSERT ON modules
FOR EACH ROW
BEGIN
    UPDATE modules SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_modules_update
AFTER UPDATE ON modules
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE modules SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

-- lessons
CREATE TRIGGER trg_lessons_insert
AFTER INSERT ON lessons
FOR EACH ROW
BEGIN
    UPDATE lessons SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_lessons_update
AFTER UPDATE ON lessons
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE lessons SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

-- sections
CREATE TRIGGER trg_sections_insert
AFTER INSERT ON sections
FOR EACH ROW
BEGIN
    UPDATE sections SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_sections_update
AFTER UPDATE ON sections
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE sections SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

-- slides
CREATE TRIGGER trg_slides_insert
AFTER INSERT ON slides
FOR EACH ROW
BEGIN
    UPDATE slides SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_slides_update
AFTER UPDATE ON slides
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE slides SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

-- quizzes
CREATE TRIGGER trg_quizzes_insert
AFTER INSERT ON quizzes
FOR EACH ROW
BEGIN
    UPDATE quizzes SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_quizzes_update
AFTER UPDATE ON quizzes
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE quizzes SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

-- quiz_questions
CREATE TRIGGER trg_quiz_questions_insert
AFTER INSERT ON quiz_questions
FOR EACH ROW
BEGIN
    UPDATE quiz_questions SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_quiz_questions_update
AFTER UPDATE ON quiz_questions
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE quiz_questions SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

-- quiz_options
CREATE TRIGGER trg_quiz_options_insert
AFTER INSERT ON quiz_options
FOR EACH ROW
BEGIN
    UPDATE quiz_options SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_quiz_options_update
AFTER UPDATE ON quiz_options
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE quiz_options SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

-- open_questions
CREATE TRIGGER trg_open_questions_insert
AFTER INSERT ON open_questions
FOR EACH ROW
BEGIN
    UPDATE open_questions SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_open_questions_update
AFTER UPDATE ON open_questions
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE open_questions SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

-- text_books
CREATE TRIGGER trg_text_books_insert
AFTER INSERT ON text_books
FOR EACH ROW
BEGIN
    UPDATE text_books SET created_at = strftime('%Y-%m-%dT%H:%M:%f', 'now'), updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;

CREATE TRIGGER trg_text_books_update
AFTER UPDATE ON text_books
WHEN OLD.updated_at = NEW.updated_at
BEGIN
    UPDATE text_books SET updated_at = strftime('%Y-%m-%dT%H:%M:%f', 'now') WHERE id = NEW.id;
END;
