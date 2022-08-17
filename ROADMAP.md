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

### 0.6 Rewrite with Connexion & Flask
- [x] 0.6.1 move from gitlab to github
  - [x] setup aleleio org on github
  - [x] single source of truth on github

- [x] 0.6.2 move to connexion
  - [x] API rebuild with OAS3.0 (Stoplight Studio)
  - [x] basic validation working
  - [x] use connexion to validate user input

- [x] 0.6.3 ORM working
  - [x] transfer and update legacy models
  - [x] set up configuration correctly

- [ ] 0.6.4 Core Logic working
  - [x] filtering games with queries
  - [x] READ game working
  - [x] CREATE game working
  - [x] DELETE game working
  - [ ] UPDATE game working
   
- [ ] 0.6.5 Testing from the start
  - [x] basic setup with pytest working
  - [x] testing with orm working
  - [ ] add test data
  - [ ] testing api endpoints
  - [ ] getting good coverage
  - [ ] github actions set up

- [ ] 0.6.6 Import/Export of Games
  - [x] get json from api-legacy
  - [x] export to markdown
  - [x] import from github
  - [x] don't overwrite existing
  - [x] add meta: licenses, refs
  - [ ] make tools work again with connexion
  - [ ] easy import to get started with development immediately

- [ ] 0.6.7 User Authentication working   
  - [ ] auth with github?
  - [ ] API keys with oauth2
  - [ ] CORS because of web/mobile?

- [ ] 0.6.8 make tools regular route (move to views/services) to facilitate automation 

- [ ] 0.6.9 Statistics working
  - [ ] add stats (private, independent) and create tools to import 
  - [ ] add api/about

- [ ] 0.6.10 API documentation with OpenAPI


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
