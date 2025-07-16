def format_timestamp(ts):
    """Format a timestamp as a string."""
    from datetime import datetime
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 