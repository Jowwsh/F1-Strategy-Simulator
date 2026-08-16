def format_secs(secs):
    hours = secs // 3600
    secs %= 3600
    mins = secs // 60
    secs %= 60
    return f"{int(hours)}:{int(mins)}:{round(secs, 3)}"