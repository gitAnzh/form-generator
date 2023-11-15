def filename_creator(referral_number, filename, string_name):
    return f'{referral_number}-{string_name}.{filename.filename.split(".")[-1]}'
