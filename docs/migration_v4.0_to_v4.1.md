# Migration Guide: Protocol v4.0 → v4.1.0

## Breaking Changes

### 1. Auto-detect Persona REMOVED
- **Before**: System automatically detected persona based on message tone
- **After**: Explicit persona selection required via `[ПАРАМЕТРЫ: persona=X]`
- **Migration**: Update all initialization calls to include `persona` parameter

### 2. Initialization Command Changed
- **Before**: Send URL without specific format
- **After**: Must use `[ПРОТОКОЛ: ЗАГРУЗИТЬ] URL [ПАРАМЕТРЫ: ...]`
- **Migration**: Wrap protocol URLs with the new command format

### 3. Remote Loading ENABLED by Default
- **Before**: Remote loading was disabled
- **After**: Remote loading automatically enabled
- **Migration**: No action needed, this is an enhancement

## Semantic Versioning Changes

### New Version Format: MAJOR.MINOR.PATCH
- **Before**: `4.0` (implicit patch 0)
- **After**: `4.1.0` (explicit patch version)

### Component Versions Synchronized
All components now share the protocol version:
- persona_system: 1.0 → 4.1.0
- craft_opt: 4.0 → 4.1.0
- All modules: 4.0 → 4.1.0

## Migration Steps

1. **Update initialization code**
   ```diff
   - Send: "https://raw.githubusercontent.com/.../core_protocol_v4.0.json"
   + Send: "[ПРОТОКОЛ: ЗАГРУЗИТЬ] https://raw.githubusercontent.com/.../core_protocol_v4.1.0.json [ПАРАМЕТРЫ: persona=A, user_name=YourName]"
   ```

2. **Remove auto-detect dependencies**
   - Delete any code that relies on automatic persona switching
   - Implement explicit persona selection logic

3. **Update module references**
   ```diff
   - [МОДУЛИ: ЗАГРУЗИТЬ file_operations_v4.0.json]
   + [МОДУЛИ: ЗАГРУЗИТЬ file_operations_v4.1.0.json]
   ```

## Rollback Plan
If issues occur, v4.0 remains available at:
`https://raw.githubusercontent.com/.../core_protocol_v4.0.json`

**Support period for v4.0**: Until 2026-06-08

## Validation
After migration, verify:
- [ ] Protocol initializes with explicit persona
- [ ] Version check passes (4.1.0)
- [ ] All modules load with compatibility check
- [ ] No auto-detection warnings

## Getting Help
- Issues: https://github.com/pbolkhovitin/ai-instructions/issues
- Docs: https://github.com/pbolkhovitin/ai-instructions/wiki
- Contact: @pbolkhovitin
