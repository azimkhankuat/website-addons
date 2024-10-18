from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _cancel_line(self, origin=None):
        res = super()._cancel_line(origin=origin)

        tickets = self.env["event.registration"].search(
            [
                ("sale_order_line_id", "in", self.ids),
                ("attendee_partner_id", "=", origin.partner_id.id),
                ("event_id", "=", self.event_id.id),
            ]
        )
        tickets.action_cancel()

        for t in tickets:
            # post a message why it was canceled
            t.message_post_with_view(
                "portal_event_tickets.message_origin_link",
                values={"origin": origin},
                subtype_id=self.env.ref("mail.mt_note").id,
            )

        return res
