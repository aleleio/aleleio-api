# Changelog

### 0.1  CRUD working
- first version, build on [Pyramid Framework](https://trypyramid.com/) in April 2019
- CRUD working: API handles incoming GET/POST/PATCH(!)/DELETE requests
- using JSON Schema to validate requests

### 0.2 auth working
- auth working: API requires api-key
- switched to git-flow model (nvie.com)

### 0.3 logging, statistics & meta
- log to console (dev) / logfile (prod)
- collect statistics on games and api usage
- move to new server

### 0.4 group needs sorting
- implement new GroupNeeds enum
- introduce weighted sorting for GroupNeeds query
- fix statistics/name counting bug
- add new User fields (0.4.1)
- add GroupNeeds Enums (0.4.1)
- add script to export/backup and reapply games (0.4.2)

### 0.5 db revisions & history
- new feature: versions (revision history)
- add update request pruning to validation
- new meta: sources & collections with own /api/endpoints
- add /api/about

# The Road Ahead

### 0.6 - Rewrite in FastAPI
- \* 0.6.0 move from gitlab to github
- 0.6.1 CRUD working
- 0.6.2 Basic validation working
- 0.6.3 Caching
- 0.6.4 Porting Functionality
- ...

> Note: Careful before updating old version. Review backup_script: user & game_meta 
> and test with web:master first, v0.5 might not be stable!

### 0.7 revise auth
- maybe oauth?
- collections of games
- complete enum implementation
        
### 0.8 basic documentation (for code, api doc for users)
- sphinx 
- caching
- code audit
- jsonschema: better error messages for e.g. game creation

### 0.9 pytest
- tests: unittest, integration test



---
**Links**

0.7
- authorization vs authentication (identity) - don't authorize admin/web with API keys?
- https://oauth.net/
- https://www.youtube.com/watch?v=mGSp-vsewxI
- https://www.youtube.com/watch?v=H6MxsFMAoP8
- https://portswigger.net/web-security/oauth

0.9
- https://chrxs.net/articles/2017/09/01/consistent-selenium-testing/
