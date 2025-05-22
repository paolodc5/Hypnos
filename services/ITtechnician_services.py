import sqlite3
from typing import List, Optional
from models.forum_question import ForumQuestion
from db.connection import get_connection


def get_all_forum_questions(conn=None) -> List[ForumQuestion]:
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM ForumQuestions ORDER BY FillingDate DESC, FillingTime DESC").fetchall()

    questions = [_row_to_forum_question(row) for row in rows]

    if close_conn:
        conn.close()

    return questions

def get_pending_forum_questions(conn=None) -> List[ForumQuestion]:
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM ForumQuestions WHERE Taken = 0 ORDER BY FillingDate DESC, FillingTime DESC").fetchall()

    questions = [_row_to_forum_question(row) for row in rows]

    if close_conn:
        conn.close()

    return questions

def mark_forum_question_as_taken(request_id: int, conn=None) -> bool:
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    cursor.execute("UPDATE ForumQuestions SET Taken = 1 WHERE RequestID = ?", (request_id,))
    conn.commit()
    success = cursor.rowcount > 0

    if close_conn:
        conn.close()

    return success

def get_forum_question_by_id(request_id: int, conn=None) -> Optional[ForumQuestion]:
    if conn is None:
        conn = get_connection()
        close_conn = True
    else:
        close_conn = False

    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM ForumQuestions WHERE RequestID = ?", (request_id,)).fetchone()

    if close_conn:
        conn.close()

    if row:
        return _row_to_forum_question(row)
    return None

def _row_to_forum_question(row: sqlite3.Row) -> ForumQuestion:
    return ForumQuestion(
        user_type=row["UserType"],
        user_id=row["UserID"],
        request_id=row["RequestID"],
        request=row["Request"],
        filling_date=row["FillingDate"],
        filling_time=row["FillingTime"],
        taken=bool(row["Taken"])
    )
