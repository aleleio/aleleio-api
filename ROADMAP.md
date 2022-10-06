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
- OpenAPI spec-first approach with Connexion framework between Aug-Oct 2022
- new license: European Union Public License
- new workflow: aleleio/teambuilding-games on github, import/export tools
- add tests: 97% coverage
- complete API documentation
- easier to get started for new contributors

# The Road Ahead

### 0.7 Document and Deploy
- [ ] 0.7.1 Import & export with fix game ids
  - [ ] Set game ids in export_to_repo
  - [ ] what happens with updates (delete&change) in the tb database? -> wipe everything and import fresh
  - [ ] Import: Make sure to not touch statistics, metadata in the existing database
- [ ] 0.7.2 Github Interaction
  - [ ] about page shows last commit datetime, links to gh repo
  - [ ] check for/set .latest_sha when TB repo is updated on Github (how?)
- [ ] 0.7.2 sentry.io
- [ ] 0.7.3 Finalize API documentation with OpenAPI 
- [ ] 0.7.4 Shut down legacy-api v0.5

### 0.8 Improve and Speedup
- caching speed up
- idea: search by name
  
### 0.9 New Toys
- collections of games
- revise auth / oauth / github (not necessary?)
- automate import/export



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
