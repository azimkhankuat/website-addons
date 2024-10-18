from odoo import fields, models
from odoo.http import request


class Event(models.Model):
    _inherit = "event.event"

    report_template_for_portal = fields.Many2one(
        "ir.actions.report", "Badge Template For Portal"
    )

    ticket_transferring = fields.Boolean(
        "Enable Ticket transferring",
        help="Attendee can transfer ticket to another partner",
        default=True,
    )

    ticket_changing = fields.Boolean(
        "Enable Ticket Changing",
        help="Attendee can change ticket to new ticket or products",
        default=True,
    )

    def check_partner_for_new_ticket(self, partner_id):
        registration = self.partner_is_participating(partner_id)
        if registration:
            ticket_order_lines = registration.mapped("sale_order_line_id")

            if request.website.sale_get_order():
                cart_refund_lines = request.website.sale_get_order().order_line.mapped(
                    lambda r: r.refund_source_line_id
                )
                # all refund lines must be in ticket_order_lines
                if all([line in cart_refund_lines for line in ticket_order_lines]):
                    # False means no errors
                    return False

        return super().check_partner_for_new_ticket(partner_id)
