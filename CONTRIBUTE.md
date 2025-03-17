# Contribute to the OCA's Odoo instance

This guide aims to help happy volunteers to contribute to the OCA's Odoo instance. I
suppose mainly the OCA's Internal Tools team.

It's split into 3 sections:

- [Concepts](#concepts): Main concepts to understand and general organization
- [Processes](#processes): Helping doing the work without missing crucial steps
- [HowTos](#howto): How to do specific tasks

## Concepts

This repository is setup as other OCA's repositories to launch CI as usual and as an
extra configuration in order to realease the OCA' Docker image used by our Odoo
instance.

Managing and freezing modules versions rely on python tools:

- [uv](https://docs.astral.sh/uv/)
- [hatch-odoo](https://pypi.org/project/hatch-odoo/)

## Processes

Here we focus on what to do without explaining how to do it.

## HowTos

Here we focus on how to do it, it's a suggest way to works but feel free to use your own
way.

### Setup developer environment

Requirements:

- Postrgesql
- [uv](https://docs.astral.sh/uv/)
- Some dependencies to be able to build some python packages: `libpq-dev`,
  `build-essential`, TODO

Prepare a python virtual environment and install the required dependencies:

```bash
uv sync
```

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
uvx --from git-aggregator gitaggregate -c repos.yaml -d ./src/ocb -p
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
