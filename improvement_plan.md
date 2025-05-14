# Plan: Fix Camera Settings Removal in AI Preset Generation (ai_prest_gen/preset_generator_engine.py)

## Goal:
To ensure that camera settings are properly excluded from generated presets for logo and traditional styles by improving the removal logic in the _process_gemini_preset_response method of the PresetGenerator class.

## Acceptance Criteria:
- The style_category is normalized (lowercased and stripped) before matching against traditional and logo categories.
- The removal of "camera_settings" keys from the "imagen_settings" dictionary is done recursively to handle nested occurrences.
- Duplicate removal code blocks are consolidated into a single, effective removal step.
- Logging or print statements are added to verify the presence and removal of camera_settings keys.
- The removal logic is applied after all merging and updates to imagen_settings.
- The fix is implemented without breaking existing functionality.

## Key Assumptions:
- The style_category passed to _process_gemini_preset_response can be normalized safely.
- The imagen_settings dictionary may contain nested dictionaries where "camera_settings" keys can appear.
- The current issue is due to shallow or incomplete removal of camera_settings keys.

## Relevant BLACKBOX.AI Features:
- Cyber Coder for code generation and modification.
- Full-Stack Agent for direct file editing.

## Relevant Technology Stack/Dependencies:
- Python 3.x
- Existing project structure and dependencies as per ai_prest_gen module.

## Potential Risks & Mitigation:
- Risk: Over-removal or unintended deletion of keys if recursive removal is too aggressive.
  Mitigation: Limit removal to keys named exactly "camera_settings" (case-insensitive).
- Risk: Changes might affect other parts of the preset generation.
  Mitigation: Thorough testing and verification of preset generation after changes.

---

## Steps:

1. Implement a helper function within PresetGenerator or as a static method to recursively remove any keys named "camera_settings" (case-insensitive) from a nested dictionary.

2. Normalize the style_category parameter by lowercasing and stripping whitespace before checking membership in traditional_categories and logo_categories lists (also normalized to lowercase).

3. Replace the existing duplicate camera_settings removal code blocks in _process_gemini_preset_response with a single call to the recursive removal function applied to final_preset["imagen_settings"] after all merging and updates.

4. Add debug print or logging statements before and after removal to confirm the presence and successful deletion of camera_settings keys.

5. Test the changes by generating presets for logo and traditional styles and verify that camera_settings no longer appear in the final presets.

6. Document the changes with comments explaining the improved removal logic.

---

## Dependent Files to be Edited:
- ai_prest_gen/preset_generator_engine.py (only _process_gemini_preset_response method and possibly helper function addition)

## Followup Steps:
- After implementation, run preset generation for affected styles to verify fix.
- If needed, update related tests or add new tests to cover this behavior.
- Confirm with user that the fix resolves the issue.

---
