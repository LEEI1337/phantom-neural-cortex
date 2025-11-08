"""
OpenAPI Documentation Generator
Exports OpenAPI 3.0 specification and generates HTML documentation
"""

import json
import yaml
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app


def export_openapi_json(output_path: Path):
    """Export OpenAPI spec as JSON."""
    openapi_schema = app.openapi()

    with open(output_path, 'w') as f:
        json.dump(openapi_schema, f, indent=2)

    print(f"✓ Exported OpenAPI JSON: {output_path}")
    return openapi_schema


def export_openapi_yaml(output_path: Path):
    """Export OpenAPI spec as YAML."""
    openapi_schema = app.openapi()

    with open(output_path, 'w') as f:
        yaml.dump(openapi_schema, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Exported OpenAPI YAML: {output_path}")


def generate_markdown_docs(openapi_schema: dict, output_path: Path):
    """Generate Markdown documentation from OpenAPI schema."""

    md = []

    # Header
    md.append(f"# {openapi_schema['info']['title']}")
    md.append(f"\n**Version:** {openapi_schema['info']['version']}")
    md.append(f"\n{openapi_schema['info']['description']}\n")

    # Table of Contents
    md.append("## Table of Contents\n")
    for tag in openapi_schema.get('tags', []):
        tag_name = tag['name']
        md.append(f"- [{tag_name.title()}](#{tag_name})")

    md.append("\n---\n")

    # Endpoints by tag
    paths = openapi_schema.get('paths', {})

    for tag in openapi_schema.get('tags', []):
        tag_name = tag['name']
        md.append(f"## {tag_name.title()}\n")
        md.append(f"{tag['description']}\n")

        # Find endpoints with this tag
        for path, methods in paths.items():
            for method, details in methods.items():
                if method in ['get', 'post', 'put', 'patch', 'delete']:
                    if tag_name in details.get('tags', []):
                        md.append(f"\n### `{method.upper()} {path}`\n")

                        # Summary and description
                        if 'summary' in details:
                            md.append(f"**{details['summary']}**\n")

                        if 'description' in details:
                            md.append(f"{details['description']}\n")

                        # Parameters
                        if 'parameters' in details:
                            md.append("\n**Parameters:**\n")
                            md.append("| Name | In | Type | Required | Description |")
                            md.append("|------|----|----- |----------|-------------|")

                            for param in details['parameters']:
                                name = param['name']
                                location = param['in']
                                schema = param.get('schema', {})
                                param_type = schema.get('type', 'string')
                                required = '✓' if param.get('required', False) else '✗'
                                desc = param.get('description', '')

                                md.append(f"| `{name}` | {location} | {param_type} | {required} | {desc} |")

                        # Request Body
                        if 'requestBody' in details:
                            md.append("\n**Request Body:**\n")
                            content = details['requestBody'].get('content', {})

                            for content_type, schema_info in content.items():
                                md.append(f"\n*Content-Type: `{content_type}`*\n")

                                if '$ref' in schema_info.get('schema', {}):
                                    ref = schema_info['schema']['$ref']
                                    schema_name = ref.split('/')[-1]
                                    md.append(f"\nSchema: `{schema_name}` (see [Schemas](#schemas))\n")

                        # Responses
                        if 'responses' in details:
                            md.append("\n**Responses:**\n")
                            md.append("| Code | Description |")
                            md.append("|------|-------------|")

                            for code, response in details['responses'].items():
                                desc = response.get('description', '')
                                md.append(f"| `{code}` | {desc} |")

                        md.append("\n")

        md.append("\n---\n")

    # Schemas
    md.append("## Schemas\n")
    schemas = openapi_schema.get('components', {}).get('schemas', {})

    for schema_name, schema_def in schemas.items():
        md.append(f"\n### {schema_name}\n")

        if 'description' in schema_def:
            md.append(f"{schema_def['description']}\n")

        if 'properties' in schema_def:
            md.append("\n**Properties:**\n")
            md.append("| Name | Type | Required | Description |")
            md.append("|------|------|----------|-------------|")

            required_fields = schema_def.get('required', [])

            for prop_name, prop_def in schema_def['properties'].items():
                prop_type = prop_def.get('type', 'object')
                is_required = '✓' if prop_name in required_fields else '✗'
                desc = prop_def.get('description', '')

                md.append(f"| `{prop_name}` | {prop_type} | {is_required} | {desc} |")

    # Write to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(md))

    print(f"✓ Generated Markdown docs: {output_path}")


def generate_postman_collection(openapi_schema: dict, output_path: Path):
    """Generate Postman collection from OpenAPI schema."""

    collection = {
        "info": {
            "name": openapi_schema['info']['title'],
            "description": openapi_schema['info']['description'],
            "version": openapi_schema['info']['version'],
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    paths = openapi_schema.get('paths', {})

    # Group by tags
    tags = {tag['name']: [] for tag in openapi_schema.get('tags', [])}

    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() in ['get', 'post', 'put', 'patch', 'delete']:
                tag = details.get('tags', ['default'])[0]

                request_item = {
                    "name": details.get('summary', f"{method.upper()} {path}"),
                    "request": {
                        "method": method.upper(),
                        "header": [],
                        "url": {
                            "raw": f"{{{{base_url}}}}{path}",
                            "host": ["{{base_url}}"],
                            "path": path.strip('/').split('/')
                        }
                    },
                    "response": []
                }

                # Add request body if present
                if 'requestBody' in details:
                    request_item['request']['header'].append({
                        "key": "Content-Type",
                        "value": "application/json"
                    })
                    request_item['request']['body'] = {
                        "mode": "raw",
                        "raw": json.dumps({}, indent=2)
                    }

                if tag in tags:
                    tags[tag].append(request_item)

    # Build collection structure
    for tag_name, items in tags.items():
        if items:
            collection['item'].append({
                "name": tag_name.title(),
                "item": items
            })

    # Add variables
    collection['variable'] = [
        {
            "key": "base_url",
            "value": "http://localhost:8000",
            "type": "string"
        }
    ]

    with open(output_path, 'w') as f:
        json.dump(collection, f, indent=2)

    print(f"✓ Generated Postman collection: {output_path}")


def main():
    """Generate all documentation formats."""
    docs_dir = Path(__file__).parent.parent.parent.parent / 'docs' / 'api'
    docs_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    print("Generating API Documentation")
    print("=" * 60 + "\n")

    # Export OpenAPI specs
    openapi_schema = export_openapi_json(docs_dir / 'openapi.json')
    export_openapi_yaml(docs_dir / 'openapi.yaml')

    # Generate Markdown docs
    generate_markdown_docs(openapi_schema, docs_dir / 'API_REFERENCE.md')

    # Generate Postman collection
    generate_postman_collection(openapi_schema, docs_dir / 'postman_collection.json')

    print("\n" + "=" * 60)
    print("Documentation Generated Successfully!")
    print("=" * 60)
    print(f"\nLocation: {docs_dir}")
    print("\nFiles created:")
    print(f"  - openapi.json          OpenAPI 3.0 specification (JSON)")
    print(f"  - openapi.yaml          OpenAPI 3.0 specification (YAML)")
    print(f"  - API_REFERENCE.md      Markdown documentation")
    print(f"  - postman_collection.json  Postman collection for testing")
    print("\nTo view interactive docs:")
    print("  1. Start backend: uvicorn main:socket_app --reload")
    print("  2. Open: http://localhost:8000/docs (Swagger UI)")
    print("  3. Or: http://localhost:8000/redoc (ReDoc)")
    print("")


if __name__ == "__main__":
    main()
