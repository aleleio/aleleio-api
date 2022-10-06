# Changelog

### 0.1 CRUD working
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

### 0.6 Rewrite with Connexion & Flask
- OpenAPI spec-first approach with Connexion framework in August 2022
- new license: European Union Public License
- new workflow: aleleio/teambuilding-games on github

# The Road Ahead

### 0.6 Rewrite with Connexion & Flask
- [x] 0.6.1 move from gitlab to github
- [x] 0.6.2 move to connexion
- [x] 0.6.3 ORM working
- [x] 0.6.4 Core Logic working (filtering, CRUD)
- [x] 0.6.5 Testing from the start (github actions, coverage)
- [x] 0.6.6 Import/Export Tools (use repo, route for automation)
- [x] 0.6.7 Authentication working, CORS added  
- [x] 0.6.8 Easier Setup for contributor onboarding
- [x] 0.6.9 Statistics working

- [ ] 0.6.10 Improve/Finalize API documentation with OpenAPI
  - [x] todo: validate with actual user
  - [x] todo: add # pragma: no cover for coverage
  - [ ] todo: aliases are not being imported? (one name per game: e.g. pipe-->atomic bomb)
  - [ ] idea: fix ids for games? every import might screw up external links
  - [ ] idea: search by name
  - [ ] todo: about page shows last commit datetime, links to gh repo


### 0.7 Document and Deploy
- docstrings complete
- implement Todos
- good enough test coverage
- logging and sentry.io
- fine-tune the readme with OpenAPI 
- shut down legacy-api v0.5

### 0.8 Improve and Speedup
- versions working again
- caching speed up
  
### 0.9 New Toys
- collections of games
- revise auth / oauth / github



---
**Links**

0.5.6, 0.9
- authorization vs authentication (identity) - don't authorize admin/web with API keys?
- https://oauth.net/
- https://www.youtube.com/watch?v=mGSp-vsewxI
- https://www.youtube.com/watch?v=H6MxsFMAoP8
- https://portswigger.net/web-security/oauth

0.9
- https://chrxs.net/articles/2017/09/01/consistent-selenium-testing/
