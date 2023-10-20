# helper functions

def path_to_upload_file(instance: object, filename: str) -> str:
    """Creates path for uploaded files."""
    return f"{instance.user.id}/files/{filename}"
