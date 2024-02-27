1. Create slack app, generate app level token, and copy Slack App Token to .env file
2. Enable socket mode
3. Add three slash commands "/chat", "/agent", and "/ask"
4. Enable event subscriptions
5. Add Bot User Events "app_mention", "app_home_opened", "message.im"
6. Under App Home enable ALways Online, Home Tab, and Messages Tab
7. OAuth & Permissions: enable scopes "channels:history", "channels:manage", "channels:read", "chat:write", "chat:write.customize", "groups:write", "im:read", "im:write", "mpim:read", "mpim:write", and "users:read"
8. Install to Workspace and copy Bot User OAuth Token to .env file
9. Pinecone index setup: 1024 dimensions, cosine metric