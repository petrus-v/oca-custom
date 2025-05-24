# Contribute to the OCA's Odoo instance

This guide aims to help happy volunteers to contribute to the OCA's Odoo instance. I
suppose mainly the OCA's Internal Tools team.

It's split into 3 sections:

- [Concepts](#concepts): Main concepts to understand and general organization
- [Processes](#processes): Helping doing the work without missing crucial steps
- [HowTos](#howto): How to do specific tasks

## Concepts

This repository is setup as other OCA's repositories to launch CI as usual and as an
extra configuration in order to build the OCA' Docker image used by our Odoo instance,
as well as facilitate the bootstrapping of a development environment.

Managing and freezing modules versions rely on python tools:

- [uv](https://docs.astral.sh/uv/)
- [hatch-odoo](https://pypi.org/project/hatch-odoo/)

## Processes

Here we focus on what to do without explaining how to do it.

### Release

- Add a tag to any git commit (prefer a commit in the 14.0 branch even this is not
  required which could helps if needs to quickly deliver a bug fix) and push it to the
  repo (ie:
  `git tag -am "New release 2025-05-24" v14.0-20250524 && git push oca v14.0-20250524`).

- This will will trigger other flow to create the docker image. Tag must matched
  following pattern to trigner the CI `v14.0.*`.

- A new docker image should be available in the
  [github docker registry](https://github.com/oca/oca-custom/pkgs/container/oca-custom)

### deployment

Ask administrator to deploy the given version.

## HowTos

Here we focus on how to do it, it's a suggest way to works but feel free to use your own
way.

### Setup developer environment

Requirements:

- Postgresql
- [uv](https://docs.astral.sh/uv/)
- Some dependencies to be able to build some python packages: `libpq-dev`,
  `build-essential`, TODO
- wkhtmltopdf

Prepare a python virtual environment with the correct python version (which uv will
download for you if necessary) and install the required dependencies:

```bash
uv sync
```

### Development

For addons living in this repository, you can just change code and restart Odoo with the
`uv run` command.

For addons in other repositories, the procedure is as follows:

- check out the repository somewhere, ie /src/\$repo
- add the following line to `pyproject.toml` in the `[tool.uv.sources]` section:

        odoo14-addon-$youraddon = { path = "/srv/$repo/setup/$youraddon", editable = true }

- run `uv sync`
- restart Odoo

### Setup database and launch tests

- setup database with demo data and all oca modules installed

```bash
uv run odoo -d oca-custom -i oca_all --stop-after-init --without-de
```

- run tests using pytest launcher

````bash
uv run pytest --odoo-database oca-custom --cov ./oca_psc_team/ oca_psc_team/
``

### Update OCB Branch

```bash
uv sync -P odoo
````

### Update a specific OCA module dependency using the latest pypi release

```bash
uv sync -P odoo14-addon-<module-name>
```

### Bump all dependencies to the latest version

```bash
uv sync -U
```
