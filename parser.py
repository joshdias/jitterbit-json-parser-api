import json

class JitterbitJSONParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.results = {
            "operations": [],
            "transformations": [],
            "scripts": [],
            "conditions": []
        }

    def parse(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._recursive_scan(data)
        return self.results

    def _recursive_scan(self, obj, parent_key=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                key_lower = key.lower()

                # Capture transformation objects
                if "transformation" in key_lower:
                    self.results["transformations"].append(key)

                # Capture scripts / JS bodies (VERY important for Jitterbit)
                if any(k in key_lower for k in ["script", "javascript", "js"]):
                    if isinstance(value, str) and value.strip():
                        self.results["scripts"].append({
                            "location": key,
                            "code": value.strip()
                        })

                # Capture conditional logic
                if "condition" in key_lower:
                    if isinstance(value, str) and value.strip():
                        self.results["conditions"].append({
                            "location": key,
                            "logic": value.strip()
                        })

                # Capture operation names
                if key_lower == "name" and parent_key.lower() == "operations":
                    self.results["operations"].append(value)

                self._recursive_scan(value, key)

        elif isinstance(obj, list):
            for item in obj:
                self._recursive_scan(item, parent_key)
