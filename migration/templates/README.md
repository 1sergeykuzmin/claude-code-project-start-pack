# Migration Templates

This directory contains template files used during framework version migrations.

## Templates

### .framework-config.template.json

Template for the runtime configuration file. Used when:
- Initializing a new project
- Resetting configuration to defaults
- Migrating from v1.x (which didn't have this file)

### settings.v2.template.json

Template for v2.0 settings.json. Used when:
- Migrating from v1.x settings format
- User wants to reset to v2.0 defaults

## Usage

### During Migration

The `/migrate` command uses these templates to:
1. Create missing files
2. Merge with existing configuration
3. Provide defaults for new fields

### Manual Reset

To reset configuration to defaults:

```bash
# Reset .framework-config
cp migration/templates/.framework-config.template.json .claude/.framework-config

# Reset settings.json (caution: loses customizations)
cp migration/templates/settings.v2.template.json .claude/settings.json
```

## Template Format

Templates use placeholder values that are replaced during migration:

| Placeholder | Replaced With |
|-------------|---------------|
| `${PROJECT_ID}` | Generated project hash |
| `${VERSION}` | Current framework version |
| `${TIMESTAMP}` | ISO-8601 timestamp |
| `${PRESET}` | User's chosen preset |

## Adding New Templates

When creating new templates:
1. Use clear placeholder syntax
2. Include all required fields
3. Document all fields with comments (JSON5 format for documentation)
4. Update this README

## Version History

| Version | Changes |
|---------|---------|
| 2.0.0 | Initial templates for v2.0 migration |
