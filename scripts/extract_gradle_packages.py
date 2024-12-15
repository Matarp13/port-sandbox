import os
import re
import json


def parse_gradle_file(file_path):
    """
    Parses a Gradle file to extract package and version details.

    Args:
        file_path (str): Path to the Gradle file.

    Returns:
        list: A list of package dictionaries with "identifier", "blueprint", and "properties".
    """
    packages = []
    try:
        with open(file_path, "r") as file:
            content = file.read()

        # Regex to match Gradle implementation dependencies
        pattern = r'implementation\s+["\']([^:]+):([^:]+):([^"\']+)["\']'
        matches = re.findall(pattern, content)

        for group, name, version in matches:
            package_name = f"{group}:{name}"
            packages.append({
                "identifier": package_name,
                "blueprint": "package",
                "properties": {
                    "package": package_name,
                    "version": version
                }
            })

    except FileNotFoundError:
        print(f"Error: Gradle file not found at {file_path}")
    except Exception as e:
        print(f"Error parsing Gradle file: {e}")

    return packages


def main():
    # Get the Gradle file path from the environment
    gradle_path = os.getenv("GRADLE_PATH")
    if not gradle_path:
        raise ValueError("GRADLE_PATH environment variable is not set.")

    # Parse the Gradle file
    packages = parse_gradle_file(gradle_path)

    # Output the packages as JSON
    print(json.dumps(packages, indent=2))


if __name__ == "__main__":
    main()
