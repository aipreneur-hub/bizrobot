from enum import Enum
class Verb(str, Enum):
    API_CALL="api.call"; WEB_FORM="web.form"; MCP_INVOKE="mcp.invoke"
    ETL="etl.transform"; FILE_GEN="file.generate"; VALIDATE="validate.schema"
