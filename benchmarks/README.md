# Benchmarks

Here a series of [locust]() script to bench mark Odoo loads in different scenarios.

## launch test

- start an odoo you want to test (not the test/production server it's the same machine,
  please!) (ie: `uv run odoo -d oca-20250828 --workers=4`)
- launch locust in a dedicated python ephemeral env (such as
  `uvx locust -f <locust_bench_file.py>`)
- go to the locust web interface and configure as desired
- launch the test !

## Analysis

### app store search

Running Odoo on my laptop with 4 workers.

#### Run 1: without change

- [Results 0 to 100 users adding 1 user every second](results/app_sotre_search/01_no_change_1_to_100.html)

#### Run 2: refactor website_app_store

In website_apps_store module, source code where calling super() and was over-writing
most of the results making a lot of useless SQL requests:
[PR OCA/apps-store#96](https://github.com/OCA/apps-store/pull/96)

- [Results 0 to 100 users adding 1 user every second](results/app_sotre_search/02_refactor_1_to_100.html)
