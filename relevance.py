# THE BRAIN: Why one agent sees a post and another doesn't
# Simple explainable logic - perfect for interviews

def calculate_relevance_score(post_text: str, agent_interests: list[str]) -> int:
    """
    Score = how many interests match the post text.
    e.g. Post: "5% off food delivery"
         Agent interests: ["food", "offers"]
         -> Score = 1 (food matches)
    """
    score = 0
    post_lower = post_text.lower()

    for interest in agent_interests:
        if interest.lower() in post_lower:
            score += 1
    return score

def should_notify(post_text: str, agent_interests: list[str]) -> bool:
    """Notify only if at least 1 interest matches."""
    return calculate_relevance_score(post_text, agent_interests) > 0

def get_relevant_agents(post_text: str, all_agents: list) -> list:
    """
    Returns list of (agent, score) sorted by highest score first.
    This is what makes it a 'Social Network' not just a chat app.
    """
    results = []
    for agent in all_agents:
        score = calculate_relevance_score(post_text, agent.interests)
        if score > 0:
            results.append((agent, score))

    # Highest relevance first
    results.sort(key=lambda x: x[1], reverse=True)
    return results