# pylint: disable=api-one-deprecated
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools

_INTERVALS = {
    "hours": lambda interval: relativedelta(hours=interval),
    "days": lambda interval: relativedelta(days=interval),
    "weeks": lambda interval: relativedelta(days=7 * interval),
    "months": lambda interval: relativedelta(months=interval),
    "now": lambda interval: relativedelta(hours=0),
}


class EventMailScheduler(models.Model):
    _inherit = "event.mail"

    interval_type = fields.Selection(
        selection_add=[
            ("transferring_started", "Transferring started"),
            ("transferring_finished", "Transferring finished"),
        ],
        ondelete={
            "transferring_started": "cascade",
            "transferring_finished": "cascade",
        },
    )

    @api.depends(
        "event_id.registration_ids.state",
        "event_id.date_begin",
        "interval_type",
        "interval_unit",
        "interval_nbr",
    )
    def _compute_scheduled_date(self):
        for rself in self:
            if rself.interval_type not in [
                "transferring_started",
                "transferring_finished",
            ]:
                super(EventMailScheduler, rself)._compute_scheduled_date()
                continue

            if rself.event_id.state not in ["confirm", "done"]:
                rself.scheduled_date = False
            else:
                date, sign = rself.event_id.create_date, 1
                rself.scheduled_date = datetime.strptime(
                    date, tools.DEFAULT_SERVER_DATETIME_FORMAT
                ) + _INTERVALS[rself.interval_unit](sign * rself.interval_nbr)
        return True

    def execute(self, registration=None):
        for rself in self:
            if rself.interval_type not in [
                "transferring_started",
                "transferring_finished",
            ]:
                super(EventMailScheduler, rself).execute()
                continue

            if registration:
                rself.write(
                    {
                        "mail_registration_ids": [
                            (0, 0, {"registration_id": registration.id})
                        ]
                    }
                )
            # execute scheduler on registrations
            rself.mail_registration_ids.filtered(
                lambda reg: reg.scheduled_date
                and reg.scheduled_date
                <= datetime.strftime(
                    fields.datetime.now(), tools.DEFAULT_SERVER_DATETIME_FORMAT
                )
            ).execute()
        return True


class EventMailRegistration(models.Model):
    _inherit = "event.mail.registration"

    @api.depends(
        "registration_id", "scheduler_id.interval_unit", "scheduler_id.interval_type"
    )
    def _compute_scheduled_date(self):
        for rself in self:
            if rself.scheduler_id.interval_type not in [
                "transferring_started",
                "transferring_finished",
            ]:
                super(EventMailRegistration, rself)._compute_scheduled_date()
                continue

            if rself.registration_id:
                # date_open is not corresponded to its meaining,
                # but keep because it's copy-pasted code
                date_open_datetime = fields.datetime.now()
                rself.scheduled_date = date_open_datetime + _INTERVALS[
                    rself.scheduler_id.interval_unit
                ](rself.scheduler_id.interval_nbr)
            else:
                rself.scheduled_date = False
        return True
