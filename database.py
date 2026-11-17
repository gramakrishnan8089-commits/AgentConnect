# Simple in-memory database - no SQL needed for placement demo
agents_db = {}
posts_db = {}
comments_db = {}

agent_counter = [1]
post_counter = [1]
comment_counter = [1]

def next_agent_id():
    id = agent_counter[0]
    agent_counter[0] += 1
    return id

def next_post_id():
    id = post_counter[0]
    post_counter[0] += 1
    return id

def next_comment_id():
    id = comment_counter[0]
    comment_counter[0] += 1
    return id