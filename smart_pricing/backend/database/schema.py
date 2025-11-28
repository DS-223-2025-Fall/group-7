"""
Schema metadata used in FastAPI OpenAPI documentation (tags, description).
"""

PROJECT_DESCRIPTION = """
Smart Pricing Backend Service.

This service enables creation of pricing experiments (projects), adding price options
(bandits), running Gaussian Thompson Sampling selection steps, submitting rewards,
and visualizing posterior distributions.
"""

TAGS_METADATA = [
    {"name": "Health", "description": "Health check endpoints"},
    {"name": "Auth", "description": "User registration & login"},
    {"name": "Projects", "description": "Manage pricing projects (CRUD)"},
    {"name": "Bandits", "description": "Manage bandits (price options)"},
    {"name": "Thompson", "description": "Thompson Sampling operations"},
]
