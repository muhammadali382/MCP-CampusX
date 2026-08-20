from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date: str, amount: int, category: str, subcategory: str="", note: str=""):
    '''Add a new expense entry to the database.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}
    
@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def update_expense(id: int, date: str=None, amount: float=None, category: str=None, subcategory: str=None, note: str=None):
    '''Update fields of an existing expense entry by id. Only provided fields are changed.'''
    fields = {
        "date": date,
        "amount": amount,
        "category": category,
        "subcategory": subcategory,
        "note": note,
    }
    updates = {k: v for k, v in fields.items() if v is not None}

    if not updates:
        return {"status": "error", "message": "No fields provided to update."}

    with sqlite3.connect(DB_PATH) as c:
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        params = list(updates.values()) + [id]

        cur = c.execute(
            f"UPDATE expenses SET {set_clause} WHERE id = ?",
            params
        )
        if cur.rowcount == 0:
            return {"status": "error", "message": f"No expense found with id {id}"}
        return {"status": "ok", "id": id, "updated_fields": updates}


@mcp.tool()
def delete_expense(id: int):
    '''Delete an expense entry by id.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE id = ?", (id,))
        if cur.rowcount == 0:
            return {"status": "error", "message": f"No expense found with id {id}"}
        return {"status": "ok", "deleted_id": id}


@mcp.tool()
def merge_categories(old_categories: list[str], new_category: str):
    '''Rename/merge one or more category labels into a single new category name.'''
    with sqlite3.connect(DB_PATH) as c:
        placeholders = ",".join("?" for _ in old_categories)
        cur = c.execute(
            f"UPDATE expenses SET category = ? WHERE category IN ({placeholders})",
            [new_category] + old_categories
        )
        return {"status": "ok", "rows_updated": cur.rowcount, "new_category": new_category}

if __name__ == "__main__":
    mcp.run()
