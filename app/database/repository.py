
import sqlite3
import json

from pathlib import Path


class MemoryRepository:

    def __init__(self, db_path="data/lesson_memory.db"):

        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.create_tables()


    def get_connection(self):

        connection = sqlite3.connect(self.db_path)

        connection.row_factory = sqlite3.Row

        connection.execute("PRAGMA foreign_keys = ON")

        return connection


    def create_tables(self):

        with self.get_connection() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS lesson_runs (

                    run_id TEXT PRIMARY KEY,

                    topic TEXT NOT NULL,

                    level TEXT NOT NULL,

                    final_status TEXT DEFAULT 'RUNNING',

                    total_attempts INTEGER DEFAULT 0,

                    final_lesson TEXT,

                    rubric_json TEXT,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS lesson_attempts (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    run_id TEXT NOT NULL,

                    attempt INTEGER NOT NULL,

                    lesson TEXT NOT NULL,

                    evaluation_results TEXT,

                    status TEXT NOT NULL,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (run_id)
                    REFERENCES lesson_runs(run_id),

                    UNIQUE(run_id, attempt)

                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS rejection_logs (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    run_id TEXT NOT NULL,

                    attempt INTEGER NOT NULL,

                    criterion_id TEXT,

                    criterion TEXT,

                    reason TEXT,

                    evidence TEXT,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (run_id)
                    REFERENCES lesson_runs(run_id)

                )
            """)


    def create_run(
        self,
        run_id,
        topic,
        level,
        rubric
    ):

        with self.get_connection() as connection:

            connection.execute("""
                INSERT INTO lesson_runs (
                    run_id,
                    topic,
                    level,
                    rubric_json
                )
                VALUES (?, ?, ?, ?)
            """, (
                run_id,
                topic,
                level,
                json.dumps(rubric)
            ))


    def save_attempt(
        self,
        run_id,
        attempt,
        lesson,
        evaluation_results,
        status
    ):

        with self.get_connection() as connection:

            connection.execute("""
                INSERT OR REPLACE INTO lesson_attempts (
                    run_id,
                    attempt,
                    lesson,
                    evaluation_results,
                    status
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                run_id,
                attempt,
                lesson,
                json.dumps(evaluation_results),
                status
            ))


    def finish_run(
        self,
        run_id,
        final_status,
        total_attempts,
        final_lesson,
        rejection_log
    ):

        with self.get_connection() as connection:

            connection.execute("""
                UPDATE lesson_runs

                SET final_status = ?,
                    total_attempts = ?,
                    final_lesson = ?

                WHERE run_id = ?
            """, (
                final_status,
                total_attempts,
                final_lesson,
                run_id
            ))

            for entry in rejection_log.get("entries", []):

                connection.execute("""
                    INSERT INTO rejection_logs (
                        run_id,
                        attempt,
                        criterion_id,
                        criterion,
                        reason,
                        evidence
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    run_id,
                    entry["attempt"],
                    entry["criterion_id"],
                    entry["criterion"],
                    entry["reason"],
                    entry["evidence"]
                ))


    def get_run_history(self, topic=None):

        with self.get_connection() as connection:

            if topic:

                rows = connection.execute("""
                    SELECT *
                    FROM lesson_runs
                    WHERE topic = ?
                    ORDER BY created_at DESC
                """, (topic,)).fetchall()

            else:

                rows = connection.execute("""
                    SELECT *
                    FROM lesson_runs
                    ORDER BY created_at DESC
                """).fetchall()

            return [dict(row) for row in rows]


    def get_attempts(self, run_id):

        with self.get_connection() as connection:

            rows = connection.execute("""
                SELECT *
                FROM lesson_attempts
                WHERE run_id = ?
                ORDER BY attempt
            """, (run_id,)).fetchall()

            return [dict(row) for row in rows]


    def get_rejections(self, run_id):

        with self.get_connection() as connection:

            rows = connection.execute("""
                SELECT *
                FROM rejection_logs
                WHERE run_id = ?
                ORDER BY attempt
            """, (run_id,)).fetchall()

            return [dict(row) for row in rows]
