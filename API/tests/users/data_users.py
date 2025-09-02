from API.utils.data import *


invalid_format_messages: {
    email_with_missing_domain_response: "address must have an @-sign",

}



email_status_code_data = {
    invalid_email: [422, email_with_missing_domain_response]
}