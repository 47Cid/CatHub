def sttf_headers(response):
    # Content Security Policy (CSP)
    csp = (
        "default-src 'self'; "
        "object-src 'none'; "
        "script-src 'none'; "
        "base-uri 'none'; "
        "style-src 'unsafe-inline'; "
        "img-src *;"
    )
    response.headers['Content-Security-Policy'] = csp

    # Add other headers as needed
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    return response


# CSP for dangling markup injection
def dmi_headers(response):
    # Content Security Policy (CSP)
    csp = (
        "script-src 'self'; "
    )
    response.headers['Content-Security-Policy'] = csp

    # Add other headers as needed
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    return response
