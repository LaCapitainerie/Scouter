class Techno(dict):
    description: str = ""
    vendor: str = ""
    type: str = ""
    product: str = ""
    version: str = ""
    assetId: str = ""
    createdAt: str = ""
    updatedAt: str = ""
    id: str = ""
    vulnerabilityCounter: int = 0
    needVulnerabilityUpdate: bool = False
    cpe: str = ""

    def __init__(self, values: dict):
        self.update(values)
        self.needVulnerabilityUpdate = False
        self.vulnerabilityCounter = 0