import os
import re
import json

def parse_plugins_from_gradle(file_path):
    """
    Parses a Gradle file to extract plugins and maps them as package entities.

    Args:
        file_path (str): Path to the Gradle file.

    Returns:
        list: A list of package entities formatted for Port's BULK_UPSERT.
    """
    entities = []

    # Regex to match plugin declarations
    plugin_pattern = re.compile(r"id\s+['\"]([^'\"]+)['\"]\s+version\s+['\"]([^'\"]+)['\"]")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            matches = plugin_pattern.findall(content)

            for plugin, version in matches:
                entities.append({
                    "identifier": plugin,
                    "blueprint": "package",
                    "properties": {
                        "package": plugin,
                        "version": version
                    }
                })

    except FileNotFoundError:
        print(f"Error: Gradle file not found at {file_path}")
    except Exception as e:
        print(f"Error parsing file: {e}")

    return entities

def main():
    gradle_path = os.getenv("GRADLE_PATH")
    if not gradle_path:
        raise ValueError("GRADLE_PATH environment variable is not set.")

    # Parse the Gradle file
    entities = parse_plugins_from_gradle(gradle_path)

    # Output the result in JSON format for Port
    print(json.dumps(entities, indent=2))

if __name__ == "__main__":
    main()
