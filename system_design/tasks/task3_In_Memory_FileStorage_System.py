class InMemoryFileStorage:
    def __init__(self):
        # Dictionary to store files {filename: content}
        self.storage = {}

    def create_file(self, filename, content):
        """Creates a new file with the given content."""
        if filename in self.storage:
            return f"Error: '{filename}' already exists."
        self.storage[filename] = content
        return f"File '{filename}' created successfully."

    def read_file(self, filename):
        """Reads and returns the file content."""
        if filename not in self.storage:
            return f"Error: '{filename}' does not exist."
        return self.storage[filename]

    def delete_file(self, filename):
        """Deletes a file from storage."""
        if filename not in self.storage:
            return f"Error: '{filename}' does not exist."
        del self.storage[filename]
        return f"File '{filename}' deleted successfully."

    def list_files(self):
        """Lists all stored files."""
        return list(self.storage.keys()) if self.storage else "No files stored."


# Example usage
if __name__ == "__main__":
    fs = InMemoryFileStorage()

    print(fs.create_file("profile.txt", "User profile data"))
    print(fs.create_file("invoice.pdf", "PDF binary data"))
    print(fs.create_file("profile.txt", "Duplicate"))  # Should fail

    print("\nAll Files:", fs.list_files())

    print("\nReading profile.txt:", fs.read_file("profile.txt"))
    print("Reading missing.txt:", fs.read_file("missing.txt"))  # Should fail

    print("\nDeleting invoice.pdf:", fs.delete_file("invoice.pdf"))
    print("Deleting invoice.pdf again:", fs.delete_file("invoice.pdf"))  # Should fail

    print("\nAll Files:", fs.list_files())
