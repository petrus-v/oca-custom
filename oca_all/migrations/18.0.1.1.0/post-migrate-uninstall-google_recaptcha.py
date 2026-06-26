import uuid

from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    env["ir.module.module"].search(
        [
            ("name", "=", "google_recaptcha"),
            ("state", "in", ("installed", "to upgrade")),
        ]
    ).button_uninstall()

    for website in env["website"].search([]):
        website.altcha_key = str(uuid.uuid4())
        website.altcha_private_key = str(uuid.uuid4())
