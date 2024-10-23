{
    "name": """Customer Event Portal""",
    "summary": """Allows to customers see their tickets for events at the Portal""",
    "category": "Marketing",
    "images": ["images/banner.jpg"],
    "version": "17.0.1.0.0",
    "author": "IT-Projects LLC",
    "support": "apps@it-projects.info",
    "website": "https://github.com/it-projects-llc/website-addons",
    "license": "AGPL-3",
    "depends": [
        "portal",
        "partner_event",
        "website_event_sale",
        "website_sale_refund",
    ],
    "data": [
        "views/portal_templates.xml",
        "views/event_registration.xml",
        "views/event_event.xml",
        "data/mail_template_data.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/portal_event_tickets/static/src/js/portal.esm.js",
        ],
        "web.assets_tests": [
            "/portal_event_tickets/static/src/js/ticket_transfer.tour.esm.js",
        ],
    },
    "qweb": [],
    "demo": ["data/res_users_demo.xml"],
}
