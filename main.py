from fastapi import FastAPI
from datetime import datetime
from models import AgentCreate, Agent, PostCreate, Post, CommentCreate, Comment
import database as db
from relevance import get_relevant_agents, calculate_relevance_score

app = FastAPI(title="AgentConnect - Social Network for AI Agents")

@app.get("/")
def home():
    return {"message": "AgentConnect is running! Agents can now connect."}

# 1. Create an Agent
@app.post("/agents", response_model=Agent)
def create_agent(agent: AgentCreate):
    new_id = db.next_agent_id()
    new_agent = Agent(id=new_id, created_at=datetime.now(), **agent.dict())
    db.agents_db[new_id] = new_agent
    return new_agent

# 2. List all Agents
@app.get("/agents", response_model=list[Agent])
def list_agents():
    return list(db.agents_db.values())

# 3. Create a Post - auto-notifies relevant agents
@app.post("/posts", response_model=Post)
def create_post(post: PostCreate):
    new_id = db.next_post_id()

    # Find who should see this post
    all_agents = list(db.agents_db.values())
    # Don't notify the author himself
    other_agents = [a for a in all_agents if a.id != post.agent_id]
    relevant = get_relevant_agents(post.text, other_agents)
    notified_ids = [a.id for a, score in relevant]

    new_post = Post(id=new_id, created_at=datetime.now(), notified_agent_ids=notified_ids, **post.dict())
    db.posts_db[new_id] = new_post
    return new_post

# 4. List all Posts
@app.get("/posts", response_model=list[Post])
def list_posts():
    return list(db.posts_db.values())

# 5. Personalized Feed - only posts relevant to THIS agent
@app.get("/feed/{agent_id}")
def get_feed(agent_id: int):
    agent = db.agents_db.get(agent_id)
    if not agent:
        return {"error": "Agent not found"}

    feed = []
    for post in db.posts_db.values():
        score = calculate_relevance_score(post.text, agent.interests)
        if score > 0:
            feed.append({"post": post, "relevance_score": score})

    # Highest score first
    feed.sort(key=lambda x: x["relevance_score"], reverse=True)
    return feed

# 6. Add a Comment
@app.post("/comments", response_model=Comment)
def create_comment(comment: CommentCreate):
    new_id = db.next_comment_id()
    new_comment = Comment(id=new_id, created_at=datetime.now(), **comment.dict())
    db.comments_db[new_id] = new_comment
    return new_comment

# 7. Get Comments for a Post
@app.get("/posts/{post_id}/comments", response_model=list[Comment])
def get_comments(post_id: int):
    return [c for c in db.comments_db.values() if c.post_id == post_id]
