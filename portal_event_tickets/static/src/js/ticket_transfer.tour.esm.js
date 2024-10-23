/** @odoo-module **/

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("ticket_transfer_receive", {
    test: true,
    url: "/my/tickets/transfer/receive",
    steps: () => [
        {
            content: "Fill attendees details",
            trigger: "input[type='email']",
            run: function () {
                // Fill:
                // * phone (optional)
                // * country_id (mandatory)
                // skip:
                // * job position (optional)
                // $("input[name='1-phone']").val("111 111");
                // $("select[name='1-country_id']").val("1");
                $("input[type='email']").val("test@test.com");
            },
        },
        {
            content: "Validate attendees details",
            trigger: 'button:contains("Confirm")',
        },
        {
            content: "We are redirected to /my/tickets page",
            trigger: ".breadcrumb-item:contains(Tickets)",
            run: function () {
                // It's needed to don't make a click on the link
            },
        },
    ],
});
