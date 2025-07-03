"""
To run this scripts use as follow

python3 ./scripts/fix_membership_line  --help
"""
import logging

import click
import click_odoo

from odoo.api import Environment

logger = logging.getLogger(__name__)


@click.command(help="Fix membership line sync date from account move line.")
@click_odoo.env_options(
    default_log_level="info",
    with_database=True,
    with_rollback=True,
)
@click.option(
    "--since",
    default="2020-01-01",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="oldest membership line to force sync",
)
@click.option(
    "--no-fix-partner", is_flag=True, help="Do not change partner on membership line"
)
def fix_membership_line(env: Environment, since: click.DateTime, no_fix_partner: bool):
    memberships = (
        env["membership.membership_line"]
        .with_context(active_test=False)
        .search(
            [
                ("date", ">=", since),
                ("account_invoice_line", "!=", False),
            ]
        )
    )

    for membership in memberships:
        messages = []
        move_line = membership.account_invoice_line
        account_member = move_line.delegated_member_id or move_line.move_id.partner_id
        if not no_fix_partner and account_member != membership.partner:
            messages.append(
                [
                    "membership line (id: %s) change "
                    "partner %s (id: %s) -> %s (id: %s)",
                    membership.id,
                    membership.partner.name,
                    membership.partner.id,
                    account_member.name,
                    account_member.id,
                ]
            )
            membership.partner = account_member
        if membership.membership_id != move_line.product_id:
            messages.append(
                [
                    "membership line (id: %s) change "
                    "product %s (id: %s) -> %s (id: %s)",
                    membership.id,
                    membership.membership_id.name,
                    membership.membership_id.id,
                    move_line.product_id.name,
                    move_line.product_id.id,
                ]
            )
            membership.membership_id = move_line.product_id
        if membership.member_price != move_line.price_unit:
            messages.append(
                [
                    "membership line (id: %s) change price %s -> %s",
                    membership.id,
                    membership.member_price,
                    move_line.price_unit,
                ]
            )
            membership.member_price = move_line.price_unit

        if membership.date_to != membership.membership_id.membership_date_to:
            messages.append(
                [
                    "membership line (id: %s) change date to %s -> %s",
                    membership.id,
                    membership.date_to,
                    membership.membership_id.membership_date_to,
                ]
            )
            membership.date_to = membership.membership_id.membership_date_to

        if messages:
            logger.info(
                "Apply %s changes while processing member %s (id: %s) - %s ",
                len(messages),
                membership.partner.name,
                membership.partner.id,
                membership.membership_id.name,
            )
            [logger.warning(*message) for message in messages]


if __name__ == "__main__":
    fix_membership_line()
