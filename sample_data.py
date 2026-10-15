"""
sample_data.py — Preloaded generic developer troubleshooting cases.
Security Guarantee: Strictly generic open-source development scenarios.
Zero sensitive, internal, or operational user data.
"""

SAMPLE_EPISODES = [
    {
        "id": "ep_jwt_refresh",
        "title": "JWT 401 Unauthorized Token Expiration in API Gateway",
        "problem": "Client requests receive HTTP 401 Unauthorized when access tokens expire after 15 minutes, causing sudden user session interruption without graceful renewal.",
        "mitigation": "Catch 401 status code in HTTP interceptor, queue concurrent requests, and request a new access token using the secure refresh cookie before retrying original requests.",
        "solution": "Configured refresh token rotation endpoint with an Axios/Fetch response interceptor that transparently refreshes expired credentials and replays queued requests.",
        "tags": "jwt, auth, api, security",
    },
    {
        "id": "ep_ssr_hydration",
        "title": "React SSR Hydration Mismatch with LocalStorage Theme",
        "problem": "Console warning 'Text content did not match server-rendered HTML' triggered by accessing window.localStorage during server-side markup generation.",
        "mitigation": "Isolate client-only state from server render pass or defer theme initialization until the component mounts in the browser DOM.",
        "solution": "Added an inline blocking script in document head to evaluate theme class before first paint, and wrapped client-only toggles in a mounted check.",
        "tags": "react, ssr, hydration, frontend",
    },
    {
        "id": "ep_docker_oom",
        "title": "Docker Container Sudden Termination with Exit Code 137",
        "problem": "Worker container suddenly crashes with exit code 137 (SIGKILL) during batch ingestion of 500MB JSON datasets due to Linux OOM killer.",
        "mitigation": "Check docker inspect .State.OOMKilled flag; replace in-memory json.load() with chunked or streaming iterators to keep memory footprint constant.",
        "solution": "Allocated 2GB memory reservation in container manifest and refactored ingestion loop to stream records via generator yield.",
        "tags": "docker, devops, memory, python",
    },
]
