class JsonValidator:
    def validate_rosters(self, data: list[dict]) -> tuple[bool, str]:
        if not isinstance(data, list):
            return False, "JSON não é lista"

        for i, item in enumerate(data):
            if not isinstance(item, dict):
                return False, f"Item {i} inválido"

            if "id" not in item or "alias" not in item:
                return False, f"Item {i} sem id/alias"

        return True, "OK"
