# Learn FastMCP - MCP Server Examples

A learning project demonstrating how to build **Model Context Protocol (MCP)** servers using **FastMCP**, a Python framework for creating MCP-compatible tools and resources.

## About This Project

This repository contains two complete MCP server implementations:
- **Demo Server** - Simple examples to learn FastMCP basics
- **Expense Tracker** - A full-featured real-world application

Perfect for understanding how to build MCP servers that can be used with Claude, other AI models, or custom applications.

---

## 📋 Server 1: Demo Server (`main.py`)

A simple starter MCP server with basic tools.

### Tools

#### `roll_dice(n_dice: int) -> list[int]`
Rolls n six-sided dice and returns the results.
```
roll_dice(3) → [4, 2, 6]
```

#### `add_numbers(a: float, b: float) -> float`
Adds two numbers and returns the sum.
```
add_numbers(5, 3) → 8
```

### Running the Demo Server
```bash
python main.py
```

---

## 💰 Server 2: Expense Tracker (`test.py`)

A comprehensive expense management MCP server with database persistence, categorization, and advanced filtering.

### Features
- SQLite database for persistent storage
- Hierarchical category system (main category + subcategory)
- Date range filtering
- Expense summarization by category
- CRUD operations (Create, Read, Update, Delete)
- Category merging/renaming

### Data Structure

Each expense entry contains:
- `id` - Unique identifier (auto-increment)
- `date` - Expense date (string format)
- `amount` - Expense amount in numeric value
- `category` - Main category (from categories.json)
- `subcategory` - Optional subcategory for detailed tracking
- `note` - Optional description/notes

### Available Categories

The expense tracker supports 12 main categories with multiple subcategories each:

- **Food** - groceries, dining out, coffee, etc.
- **Transport** - fuel, public transport, cab/ride-hailing, parking, tolls
- **Housing** - rent, maintenance, property tax, repairs, furnishing
- **Utilities** - electricity, water, gas, internet, mobile, TV
- **Health** - medicines, doctor consultation, diagnostics, fitness
- **Education** - books, courses, online subscriptions, exam fees
- **Family & Kids** - school fees, daycare, toys, events
- **Entertainment** - movies, streaming subscriptions, gaming, outings
- **Shopping** - clothing, footwear, electronics, appliances, home décor
- **Subscriptions** - SaaS tools, cloud/AI, music, storage, newsletters
- **Personal Care** - salon, grooming, cosmetics, hygiene
- **Gifts & Donations** - personal gifts, charity, festival gifts
- **Finance & Fees** - bank fees, investment fees, etc.

### Tools

#### `add_expense(date: str, amount: int, category: str, subcategory: str = "", note: str = "")`
Add a new expense entry to the database.
```json
{
  "date": "2026-08-20",
  "amount": 45,
  "category": "food",
  "subcategory": "dining_out",
  "note": "Lunch with friends"
}
```
Returns: `{"status": "ok", "id": 1}`

#### `list_expenses(start_date: str, end_date: str)`
List all expenses within an inclusive date range (YYYY-MM-DD format).
```
list_expenses("2026-08-01", "2026-08-31")
```
Returns array of expense records with all fields.

#### `summarize(start_date: str, end_date: str, category: str = None)`
Get total amount spent by category within a date range. Optionally filter by a specific category.
```
summarize("2026-08-01", "2026-08-31")
summarize("2026-08-01", "2026-08-31", "food")
```
Returns:
```json
[
  {"category": "food", "total_amount": 150},
  {"category": "transport", "total_amount": 50}
]
```

#### `update_expense(id: int, date: str = None, amount: float = None, category: str = None, subcategory: str = None, note: str = None)`
Update specific fields of an existing expense. Only provided fields are modified.
```
update_expense(1, amount=50, note="Updated note")
```
Returns: `{"status": "ok", "id": 1, "updated_fields": {...}}`

#### `delete_expense(id: int)`
Delete an expense entry by id.
```
delete_expense(1)
```
Returns: `{"status": "ok", "deleted_id": 1}`

#### `merge_categories(old_categories: list[str], new_category: str)`
Rename or merge one or more category labels into a single new category. Useful for consolidating expense categories.
```
merge_categories(["food", "dining"], "meals")
```
Returns: `{"status": "ok", "rows_updated": 15, "new_category": "meals"}`

### Resources

#### `expense://categories`
Returns the categories structure as JSON. This resource is read fresh each time, so you can edit `categories.json` without restarting the server.

### Running the Expense Tracker
```bash
python test.py
```

**Database**: Creates `expenses.db` in the same directory for persistent storage.

---

## Installation & Setup

### Prerequisites
- Python 3.14+
- FastMCP 3.4.7+

### Install Dependencies
```bash
pip install fastmcp>=3.4.7
```

Or using the project's pyproject.toml:
```bash
pip install -e .
```

---

## Project Structure

```
learn-fastmcp/
├── main.py              # Demo server (roll_dice, add_numbers)
├── test.py              # Expense Tracker server (full MCP implementation)
├── categories.json      # Category definitions for expense tracker
├── expenses.db          # SQLite database (auto-created by test.py)
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

---

## Learning Path

1. **Start with `main.py`** to understand the basics:
   - How to create a FastMCP instance
   - How to define simple tools with `@mcp.tool` decorator
   - How to run the server with `mcp.run()`

2. **Progress to `test.py`** to learn advanced patterns:
   - SQLite database integration
   - File I/O and resource management
   - Complex tool logic (CRUD operations)
   - Resources with `@mcp.resource` decorator
   - Optional and conditional parameters
   - Error handling and validation

---

## Key FastMCP Concepts

### Tools
Functions decorated with `@mcp.tool()` that can be called by MCP clients. Each tool has:
- Input parameters with type hints
- A docstring describing functionality
- A return value

### Resources
Static or dynamic content accessible via URI. Defined with `@mcp.resource()`:
- Identified by a unique URI (e.g., `expense://categories`)
- Optionally specify MIME type
- Can read from files or compute dynamically

### Server Lifecycle
```python
mcp = FastMCP("ServerName")  # Create instance

@mcp.tool()                  # Define tools
def my_tool(): ...

if __name__ == "__main__":
    mcp.run()               # Start the server
```

---

## Next Steps

- Modify the demo server to add new tools
- Extend the expense tracker with new features (e.g., budgets, recurring expenses)
- Create your own MCP server for a domain you're interested in
- Connect your MCP server to Claude using the MCP protocol

---

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Python Typing Documentation](https://docs.python.org/3/library/typing.html)

---

**Happy learning! 🚀**
