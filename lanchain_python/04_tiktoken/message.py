class Message:
    def __init__(self, role: str, content: str, name: str = None):
        # The constructor for the Message class.
        # :param role: A string indicating the role of the message (e.g., 'system' or 'human').
        # :param content: The actual text content of the message.
        # :param name: An optional string that represents the name associated with the message, default is None.

        # Initialize the role of the message.
        self.role = role
        # Initialize the content of the message.
        self.content = content
        # Initialize the name associated with the message, if provided.
        self.name = name
