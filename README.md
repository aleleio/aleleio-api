# alele.io | API Component

<p>
    <a href="https://codeclimate.com/github/aleleio/aleleio-api/maintainability"><img src="https://api.codeclimate.com/v1/badges/20a1737cd92ebee54db5/maintainability" /></a>
    <a href="https://codeclimate.com/github/aleleio/aleleio-api/test_coverage"><img src="https://api.codeclimate.com/v1/badges/20a1737cd92ebee54db5/test_coverage" /></a>
    <a href="LICENSE"><img src="https://badgen.net/github/license/aleleio/aleleio-api" /></a>
</p>

[alele.io](https://alele.io) is a public database of teambuilding games. The database is wrapped in a REST API
(this repository!) which is available at [alele.io/api](https://alele.io/api) and can be accessed through the web
and mobile devices. It's a labour of love and relies on its community to survive and thrive.

### Getting Started

The API Component uses Python [3.10](.python-version) to run its stack:

* API-first design driven by [Connexion](https://github.com/spec-first/connexion) with [Flask](https://flask.palletsprojects.com)
* open standards using [OpenAPI Specification 3.0](https://openapis.org)
* database access through [PonyORM](https://ponyorm.org/)
* testing with [pytest](https://docs.pytest.org)

In order to get things running, have a look at [CONTRIBUTING](CONTRIBUTING.md).

### Teambuilding Games Database

The single source of truth for [alele.io](https://alele.io) is not the database but the [aleleio teambuilding-games repository](https://github.com/aleleio/teambuilding-games). To update the games, please fork that repository and create a pull request.

### License

Please know, that the source code of the alele.io API component is [licensed under the European Union Public License](LICENSE) so that you may enjoy its inner workings without restrictions! This also ensures that your contribution will not be used for closed-source projects as it must be redistributed with a compatible copy-left license. You can read the EUPL [in your language](https://eupl.eu/) - you should, it's great!

Thank you for considering to help in the first place! You're awesome! :star2:



