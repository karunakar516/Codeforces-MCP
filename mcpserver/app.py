from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP(
    name="CodeforcesMCPServer",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8000,  # only used for SSE transport (set this to any port)
)

# Constants
CODEFORCES_API_BASE = "https://codeforces.com/api"


async def make_api_request(endpoint: str, params: dict[str, Any] = None) -> dict[str, Any] | None:
    """Make a request to the Codeforces API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            url = f"{CODEFORCES_API_BASE}/{endpoint}"
            response = await client.get(url, params=params or {}, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making API request: {e}")
            return None


def format_codeforces_profile(profile: dict) -> str:
    """Format a Codeforces profile into a readable string."""
    return f"""Handle: {profile.get('handle', 'Unknown')}
Name: {profile.get('firstName', '')} {profile.get('lastName', '')}
Rating: {profile.get('rating', 'Unrated')}
Rank: {profile.get('rank', 'Unranked')}
Max Rating: {profile.get('maxRating', 'N/A')}
Max Rank: {profile.get('maxRank', 'N/A')}
Country: {profile.get('country', 'Unknown')}
City: {profile.get('city', 'Unknown')}
Organization: {profile.get('organization', 'None')}
Contribution: {profile.get('contribution', 0)}
Friend Count: {profile.get('friendOfCount', 0)}"""


def format_blog_entry(entry: dict) -> str:
    """Format a blog entry into a readable string."""
    return f"""ID: {entry.get('id', 'N/A')}
Title: {entry.get('title', 'No Title')}
Author: {entry.get('authorHandle', 'Unknown')}
Creation Time: {entry.get('creationTimeSeconds', 'N/A')}
Rating: {entry.get('rating', 0)}
Tags: {', '.join(entry.get('tags', []))}"""


def format_contest(contest: dict) -> str:
    """Format a contest into a readable string."""
    return f"""ID: {contest.get('id', 'N/A')}
Name: {contest.get('name', 'No Name')}
Type: {contest.get('type', 'Unknown')}
Phase: {contest.get('phase', 'Unknown')}
Duration: {contest.get('durationSeconds', 0)} seconds
Start Time: {contest.get('startTimeSeconds', 'N/A')}
Difficulty: {contest.get('difficulty', 'N/A')}"""


def format_problem(problem: dict) -> str:
    """Format a problem into a readable string."""
    return f"""Contest ID: {problem.get('contestId', 'N/A')}
Index: {problem.get('index', 'N/A')}
Name: {problem.get('name', 'No Name')}
Type: {problem.get('type', 'Unknown')}
Points: {problem.get('points', 'N/A')}
Rating: {problem.get('rating', 'Unrated')}
Tags: {', '.join(problem.get('tags', []))}"""


def format_submission(submission: dict) -> str:
    """Format a submission into a readable string."""
    return f"""ID: {submission.get('id', 'N/A')}
Contest ID: {submission.get('contestId', 'N/A')}
Problem: {submission.get('problem', {}).get('index', 'N/A')} - {submission.get('problem', {}).get('name', 'No Name')}
Author: {submission.get('author', {}).get('members', [{}])[0].get('handle', 'Unknown') if submission.get('author', {}).get('members') else 'Unknown'}
Programming Language: {submission.get('programmingLanguage', 'Unknown')}
Verdict: {submission.get('verdict', 'Unknown')}
Time Consumed: {submission.get('timeConsumedMillis', 0)} ms
Memory Consumed: {submission.get('memoryConsumedBytes', 0)} bytes
Creation Time: {submission.get('creationTimeSeconds', 'N/A')}"""


# Blog Entry APIs
@mcp.tool()
async def get_blog_comments(blog_entry_id: int) -> str:
    """Get comments for a specific blog entry.
    
    Args:
        blog_entry_id: ID of the blog entry
    """
    data = await make_api_request("blogEntry.comments", {"blogEntryId": blog_entry_id})
    
    if not data or "result" not in data:
        return "Unable to fetch blog comments."
    
    if not data["result"]:
        return "No comments found."
    
    comments = []
    for comment in data["result"]:
        comments.append(f"""ID: {comment.get('id', 'N/A')}
Author: {comment.get('commentatorHandle', 'Unknown')}
Text: {comment.get('text', 'No text')[:200]}...
Creation Time: {comment.get('creationTimeSeconds', 'N/A')}
Rating: {comment.get('rating', 0)}""")
    
    return "\n---\n".join(comments)


@mcp.tool()
async def get_blog_entry(blog_entry_id: int) -> str:
    """Get a specific blog entry.
    
    Args:
        blog_entry_id: ID of the blog entry
    """
    data = await make_api_request("blogEntry.view", {"blogEntryId": blog_entry_id})
    
    if not data or "result" not in data:
        return "Unable to fetch blog entry."
    
    entry = data["result"]
    return f"""{format_blog_entry(entry)}
Content: {entry.get('text', 'No content')[:500]}..."""


# Contest APIs
@mcp.tool()
async def get_contest_hacks(contest_id: int, as_manager: bool = False) -> str:
    """Get hacks for a specific contest.
    
    Args:
        contest_id: ID of the contest
        as_manager: Whether to get manager-level information
    """
    params = {"contestId": contest_id}
    if as_manager:
        params["asManager"] = "true"
    
    data = await make_api_request("contest.hacks", params)
    
    if not data or "result" not in data:
        return "Unable to fetch contest hacks."
    
    if not data["result"]:
        return "No hacks found."
    
    hacks = []
    for hack in data["result"]:
        hacks.append(f"""ID: {hack.get('id', 'N/A')}
Hacker: {hack.get('hacker', {}).get('handle', 'Unknown')}
Defender: {hack.get('defender', {}).get('handle', 'Unknown')}
Problem: {hack.get('problem', {}).get('index', 'N/A')}
Verdict: {hack.get('verdict', 'Unknown')}
Creation Time: {hack.get('creationTimeSeconds', 'N/A')}""")
    
    return "\n---\n".join(hacks)


@mcp.tool()
async def get_contest_list(gym: bool = False, group_code: Optional[str] = None) -> str:
    """Get list of contests.
    
    Args:
        gym: Whether to get gym contests
        group_code: Group code to filter contests
    """
    params = {}
    if gym:
        params["gym"] = "true"
    if group_code:
        params["groupCode"] = group_code
    
    data = await make_api_request("contest.list", params)
    
    if not data or "result" not in data:
        return "Unable to fetch contest list."
    
    if not data["result"]:
        return "No contests found."
    
    contests = [format_contest(contest) for contest in data["result"][:20]]  # Limit to first 20
    return "\n---\n".join(contests)


@mcp.tool()
async def get_contest_rating_changes(contest_id: int) -> str:
    """Get rating changes for a specific contest.
    
    Args:
        contest_id: ID of the contest
    """
    data = await make_api_request("contest.ratingChanges", {"contestId": contest_id})
    
    if not data or "result" not in data:
        return "Unable to fetch rating changes."
    
    if not data["result"]:
        return "No rating changes found."
    
    changes = []
    for change in data["result"][:50]:  # Limit to first 50
        changes.append(f"""Handle: {change.get('handle', 'Unknown')}
Rank: {change.get('rank', 'N/A')}
Old Rating: {change.get('oldRating', 'N/A')}
New Rating: {change.get('newRating', 'N/A')}""")
    
    return "\n---\n".join(changes)


@mcp.tool()
async def get_contest_standings(contest_id: int, from_rank: int = 1, count: int = 10, 
                               handles: Optional[str] = None, show_unofficial: bool = False) -> str:
    """Get contest standings.
    
    Args:
        contest_id: ID of the contest
        from_rank: Starting rank (1-based)
        count: Number of standings to return
        handles: Semicolon-separated list of handles
        show_unofficial: Whether to show unofficial participants
    """
    params = {"contestId": contest_id, "from": from_rank, "count": count}
    if handles:
        params["handles"] = handles
    if show_unofficial:
        params["showUnofficial"] = "true"
    
    data = await make_api_request("contest.standings", params)
    
    if not data or "result" not in data:
        return "Unable to fetch contest standings."
    
    result = data["result"]
    contest_info = format_contest(result.get("contest", {}))
    
    standings = []
    for row in result.get("rows", []):
        party = row.get("party", {})
        handle = party.get("members", [{}])[0].get("handle", "Unknown") if party.get("members") else "Unknown"
        standings.append(f"""Rank: {row.get('rank', 'N/A')}
Handle: {handle}
Points: {row.get('points', 0)}
Penalty: {row.get('penalty', 0)}
Successful Hacks: {row.get('successfulHackCount', 0)}
Unsuccessful Hacks: {row.get('unsuccessfulHackCount', 0)}""")
    
    return f"Contest Info:\n{contest_info}\n\nStandings:\n" + "\n---\n".join(standings)


@mcp.tool()
async def get_contest_status(contest_id: int, handle: Optional[str] = None, 
                           from_sub: int = 1, count: int = 10) -> str:
    """Get contest submissions.
    
    Args:
        contest_id: ID of the contest
        handle: Specific user handle
        from_sub: Starting submission index (1-based)
        count: Number of submissions to return
    """
    params = {"contestId": contest_id, "from": from_sub, "count": count}
    if handle:
        params["handle"] = handle
    
    data = await make_api_request("contest.status", params)
    
    if not data or "result" not in data:
        return "Unable to fetch contest submissions."
    
    if not data["result"]:
        return "No submissions found."
    
    submissions = [format_submission(sub) for sub in data["result"]]
    return "\n---\n".join(submissions)


# Problemset APIs
@mcp.tool()
async def get_problemset_problems(tags: Optional[str] = None, problemset_name: Optional[str] = None) -> str:
    """Get problems from problemset.
    
    Args:
        tags: Semicolon-separated list of tags
        problemset_name: Custom problemset name
    """
    params = {}
    if tags:
        params["tags"] = tags
    if problemset_name:
        params["problemsetName"] = problemset_name
    
    data = await make_api_request("problemset.problems", params)
    
    if not data or "result" not in data:
        return "Unable to fetch problems."
    
    problems = data["result"].get("problems", [])
    if not problems:
        return "No problems found."
    
    formatted_problems = [format_problem(problem) for problem in problems[:50]]  # Limit to first 50
    return "\n---\n".join(formatted_problems)


@mcp.tool()
async def get_problemset_recent_status(count: int = 10, problemset_name: Optional[str] = None) -> str:
    """Get recent submissions from problemset.
    
    Args:
        count: Number of submissions to return (max 1000)
        problemset_name: Custom problemset name
    """
    params = {"count": min(count, 1000)}
    if problemset_name:
        params["problemsetName"] = problemset_name
    
    data = await make_api_request("problemset.recentStatus", params)
    
    if not data or "result" not in data:
        return "Unable to fetch recent submissions."
    
    if not data["result"]:
        return "No submissions found."
    
    submissions = [format_submission(sub) for sub in data["result"]]
    return "\n---\n".join(submissions)


# Recent Actions API
@mcp.tool()
async def get_recent_actions(max_count: int = 30) -> str:
    """Get recent actions.
    
    Args:
        max_count: Number of recent actions to return (max 100)
    """
    data = await make_api_request("recentActions", {"maxCount": min(max_count, 100)})
    
    if not data or "result" not in data:
        return "Unable to fetch recent actions."
    
    if not data["result"]:
        return "No recent actions found."
    
    actions = []
    for action in data["result"]:
        actions.append(f"""Time: {action.get('timeSeconds', 'N/A')}
Blog Entry: {action.get('blogEntry', {}).get('title', 'No Title')}
Comment: {action.get('comment', {}).get('text', 'No comment')[:100] if action.get('comment') else 'N/A'}...""")
    
    return "\n---\n".join(actions)


# User APIs
@mcp.tool()
async def get_user_profiles(handles: str, check_historic_handles: bool = True) -> str:
    """Get profiles for a list of users.

    Args:
        handles: Semicolon-separated list of handles
        check_historic_handles: Whether to check historic handle changes
    """
    params = {"handles": handles.replace(",", ";")}
    if not check_historic_handles:
        params["checkHistoricHandles"] = "false"
    
    data = await make_api_request("user.info", params)

    if not data or "result" not in data:
        return "Unable to fetch profiles or no profiles found."

    if not data["result"]:
        return "No profiles found."

    profiles = [format_codeforces_profile(profile) for profile in data["result"]]
    return "\n---\n".join(profiles)


@mcp.tool()
async def get_user_blog_entries(handle: str) -> str:
    """Get user's blog entries.
    
    Args:
        handle: Codeforces user handle
    """
    data = await make_api_request("user.blogEntries", {"handle": handle})
    
    if not data or "result" not in data:
        return "Unable to fetch blog entries."
    
    if not data["result"]:
        return "No blog entries found."
    
    entries = [format_blog_entry(entry) for entry in data["result"]]
    return "\n---\n".join(entries)


@mcp.tool()
async def get_user_rated_list(active_only: bool = False, include_retired: bool = True, 
                             contest_id: Optional[int] = None) -> str:
    """Get list of rated users.
    
    Args:
        active_only: Whether to return only recently active users
        include_retired: Whether to include retired users
        contest_id: Specific contest ID to filter by
    """
    params = {}
    if active_only:
        params["activeOnly"] = "true"
    if not include_retired:
        params["includeRetired"] = "false"
    if contest_id:
        params["contestId"] = contest_id
    
    data = await make_api_request("user.ratedList", params)
    
    if not data or "result" not in data:
        return "Unable to fetch rated users."
    
    if not data["result"]:
        return "No rated users found."
    
    users = [format_codeforces_profile(user) for user in data["result"][:50]]  # Limit to first 50
    return "\n---\n".join(users)


@mcp.tool()
async def get_user_rating_history(handle: str) -> str:
    """Get user's rating history.
    
    Args:
        handle: Codeforces user handle
    """
    data = await make_api_request("user.rating", {"handle": handle})
    
    if not data or "result" not in data:
        return "Unable to fetch rating history."
    
    if not data["result"]:
        return "No rating history found."
    
    history = []
    for change in data["result"]:
        history.append(f"""Contest: {change.get('contestName', 'Unknown')}
Rank: {change.get('rank', 'N/A')}
Old Rating: {change.get('oldRating', 'N/A')}
New Rating: {change.get('newRating', 'N/A')}
Contest Time: {change.get('ratingUpdateTimeSeconds', 'N/A')}""")
    
    return "\n---\n".join(history)


@mcp.tool()
async def get_user_submissions(handle: str, from_sub: int = 1, count: int = 10) -> str:
    """Get user's submissions.
    
    Args:
        handle: Codeforces user handle
        from_sub: Starting submission index (1-based)
        count: Number of submissions to return
    """
    params = {"handle": handle, "from": from_sub, "count": count}
    
    data = await make_api_request("user.status", params)
    
    if not data or "result" not in data:
        return "Unable to fetch user submissions."
    
    if not data["result"]:
        return "No submissions found."
    
    submissions = [format_submission(sub) for sub in data["result"]]
    return "\n---\n".join(submissions)


if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")