# Project Overview

This project contains two main components:

- **mcpserver**: A Codeforces MCP server exposing contest, user, and problem APIs.
- **interactive-chat-bot**: An interactive chat bot client that connects to an MCP server and enables conversational querying.

---

## Folder Structure

```
.
├── mcpserver/
│   ├── app.py
│   ├── client.py
│   ├── requirements.txt
│   └── Dockerfile
├── interactive-chat-bot/
│   ├── app.py
│   ├── client.py
│   └── config.json
├── README.md
└── ...
```

---

## mcpserver

### Description

- Implements an MCP server for Codeforces data (contests, users, problems, etc.).
- Exposes tools via the MCP protocol (SSE or stdio).
- Can be run locally or in Docker.

### Setup

#### 1. Install dependencies

```bash
cd mcpserver
pip install -r requirements.txt
```
Or, using [uv](https://github.com/astral-sh/uv):
```bash
uv pip install -r requirements.txt
```

#### 2. Run the server

```bash
uv run app.py
```
- By default, runs on `localhost:8000` with SSE transport.

#### 3. Docker (optional)

Build and run the server in Docker:
```bash
cd mcpserver
docker build -t mcpserver .
docker run -p 8000:8000 mcpserver
```

#### 4. Test the server

You can use the provided `client.py` to test the server:
```bash
python client.py
```
- Make sure the server is running before running the client.

---

## Tools Provided by the MCP Server

The MCP server exposes a variety of tools for interacting with Codeforces data. Below is a summary of the available tools and their purposes:

### Blog Entry tools

- **get_blog_comments(blog_entry_id)**  
  Get comments for a specific blog entry.

- **get_blog_entry(blog_entry_id)**  
  Get the details and content of a specific blog entry.

---

### Contest tools

- **get_contest_hacks(contest_id, as_manager=False)**  
  Get hacks for a specific contest.

- **get_contest_list(gym=False, group_code=None)**  
  Get a list of contests (optionally filter by gym or group).

- **get_contest_rating_changes(contest_id)**  
  Get rating changes for a specific contest.

- **get_contest_standings(contest_id, from_rank=1, count=10, handles=None, show_unofficial=False)**  
  Get contest standings, optionally filtered by user handles or unofficial participants.

- **get_contest_status(contest_id, handle=None, from_sub=1, count=10)**  
  Get contest submissions, optionally filtered by user handle.

---

### Problemset tools

- **get_problemset_problems(tags=None, problemset_name=None)**  
  Get problems from the problemset, optionally filtered by tags or custom problemset name.

- **get_problemset_recent_status(count=10, problemset_name=None)**  
  Get recent submissions from the problemset.

---

### Recent Actions tools

- **get_recent_actions(max_count=30)**  
  Get recent actions (blog posts, comments, etc.) on Codeforces.

---

### User tools

- **get_user_profiles(handles, check_historic_handles=True)**  
  Get profiles for a list of users (handles separated by semicolons).

- **get_user_blog_entries(handle)**  
  Get blog entries for a specific user.

- **get_user_rated_list(active_only=False, include_retired=True, contest_id=None)**  
  Get a list of rated users, optionally filtered by activity, retirement status, or contest.

- **get_user_rating_history(handle)**  
  Get the rating history for a specific user.

- **get_user_submissions(handle, from_sub=1, count=10)**  
  Get submissions for a specific user.

---

**Usage:**  
You can call these tools from any MCP client (such as the provided `client.py` or the interactive chat bot) by specifying the tool name and required arguments.

---

## Example Usage Showcase

Below are real examples of how you can interact with the interactive chat bot and the MCP server tools:

```
$ python client.py
Initializing chat...

===== Interactive MCP Chat =====
Type 'exit' or 'quit' to end the conversation
Type 'clear' to clear conversation history
==================================

You: hey

Assistant: Hello! How can I assist you today? 😊

You: can you fetch codeforces profile of karunakar_516 and sriramadari

Assistant: Here are the profiles for the requested Codeforces handles:

**karunakar_516 (Karunakar Balivada):**
- **Current Rating:** 1645 (Expert)
- **Max Rating:** 1664 (Expert)
- **Location:** Visakhapatnam, India
- **Organization:** Vignan's Institute of Information Technology
- **Contribution:** 5
- **Friends:** 34 friends

**sriramadari (SRIRAMADARI):**
- **Current Rating:** 956 (Newbie)
- **Max Rating:** 956 (Newbie)
- **Location:** Unknown
- **Organization:** None
- **Contribution:** 0
- **Friends:** 5 friends

---

You: get recent contest performances by  karunakar_516   

Assistant: Here's the recent contest performance history for **karunakar_516**, based on their rating changes and contest participation (most recent first):

### **Latest Contests (Most Recent First):**
1. **Educational Codeforces Round 175 (Rated for Div. 2)**
   - **Rank:** 2414
   - **Old Rating:** 1664
   - **New Rating:** 1645

2. **Codeforces Round 1006 (Div. 3)**
   - **Rank:** 369
   - **Old Rating:** 1583
   - **New Rating:** 1664

3. **Codeforces Round 1005 (Div. 2)**
   - **Rank:** 2414
   - **Old Rating:** 1546
   - **New Rating:** 1583

4. **Codeforces Round 1004 (Div. 2)**
   - **Rank:** 1100
   - **Old Rating:** 1543
   - **New Rating:** 1593

5. **Codeforces Round 1000 (Div. 2)**
   - **Rank:** 3961
   - **Old Rating:** 1543
   - **New Rating:** 1552

---

You: what all tools do you have access to?

Assistant: I have access to the following **Codeforces API tools** to retrieve data:

### Blog Tools
1. **`get_blog_comments`**
   *Fetch comments for a specific blog entry.*
   Args: `blog_entry_id`

2. **`get_blog_entry`**
   *Get details of a specific blog entry.*
   Args: `blog_entry_id`

### Contest Tools
3. **`get_contest_hacks`**
   *Retrieve hacks for a contest (requires contest ID).*
   Args: `contest_id`, `as_manager` (optional)

4. **`get_contest_list`**
   *List contests, including gyms or by group code.*
   Args: `gym`, `group_code`

5. **`get_contest_rating_changes`**
   *Get rating changes for a contest.*
   Args: `contest_id`

6. **`get_contest_standings`**
   *Fetch contest rankings/participant data.*
   Args: `contest_id`, `from_rank`, `count`, `handles`, `show_unofficial`

7. **`get_contest_status`**
   *Retrieve submissions for a contest.*
   Args: `contest_id`, `handle`, `from_sub`, `count`

### Problem Tools
8. **`get_problemset_problems`**
   *Get problems by tags or problemset name.*
   Args: `tags`, `problemset_name`

9. **`get_problemset_recent_status`**
   *Fetch recent submissions for a problemset.*
   Args: `count`, `problemset_name`

### User Tools
10. **`get_user_profiles`**
    *Get profiles for multiple users.*
    Args: `handles` (semicolon-separated), `check_historic_handles`

11. **`get_user_blog_entries`**
    *List a user's blog entries.*
    Args: `handle`

12. **`get_user_rated_list`**
    *List rated users (filter by contest or settings).*
    Args: `active_only`, `contest_id`, `include_retired`

13. **`get_user_rating_history`**
    *Get a user's rating changes over time.*
    Args: `handle`

14. **`get_user_submissions`**
    *Fetch a user's recent submissions.*
    Args: `handle`, `from_sub`, `count`

### Miscellaneous
15. **`get_recent_actions`**
    *View recent platform-wide actions (e.g., new blogs, system updates).*
    Args: `max_count`

---

You can ask for Codeforces data in natural language, and the bot will use the appropriate tool!

---

## interactive-chat-bot

### Description

- Provides an interactive chat interface to query an MCP server (such as the one in `mcpserver`).
- Uses LangChain and Groq for LLM-powered conversations.
- Configurable via `config.json`.

### Setup

#### 1. Install dependencies

Make sure you have the required packages (LangChain, Groq, MCP client, etc.) installed in your environment.

#### 2. Configure

Edit `config.json` to point to your MCP server. Example:
```json
{
    "mcpServers": {
        "weather": {
            "command": "uv",
            "args": [
                "run",
                "--with",
                "mcp[cli]",
                "mcp",
                "run",
                "<path to your app.py>"
            ]
        }
    }
}
```

#### 3. Run the chat bot

```bash
python client.py
```
- This will start an interactive chat session.
- Type your questions and interact with the MCP server.
- Type `exit` or `quit` to end the session, or `clear` to clear conversation history.

#### 4. Environment Variables

- If using Groq or other LLMs, set the required API keys in your environment or a `.env` file.

---

## Tips

- Ensure the MCP server is running before starting the chat bot.
- You can modify or extend the tools in `app.py` in either folder to add more capabilities.
- For development, you can run both the server and the chat bot locally in separate terminals.

---
