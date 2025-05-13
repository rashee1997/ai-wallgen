# ai_prest_gen/data_models.py
"""
Pydantic models for validating the structure of AI-generated presets.
Includes models for all identified specific style settings groups.
"""
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field, validator

# --- Common Nested Models ---

class CameraSettings(BaseModel):
    camera_model: Optional[str] = None
    lens_type: Optional[str] = None
    aperture: Optional[str] = None
    focal_length: Optional[str] = None
    shutter_speed: Optional[str] = None
    iso: Optional[str] = None
    filter_type: Optional[str] = None
    depth_of_field: Optional[str] = None
    white_balance: Optional[str] = None
    focus_mode: Optional[str] = None
    exposure_mode: Optional[str] = None
    image_stabilization: Optional[str] = None
    metering_mode: Optional[str] = None
    flash_mode: Optional[str] = None
    shooting_mode: Optional[str] = None
    focus_point_selection: Optional[str] = None
    image_format: Optional[str] = None
    color_space: Optional[str] = None
    field_of_view: Optional[str] = None
    camera_type: Optional[str] = None

class StyleSettings(BaseModel):
    art_movement: Optional[str] = None
    post_processing: List[str] = Field(default_factory=list)
    style_era: Optional[str] = None
    photo_style: Optional[str] = None
    drawing_approach: Optional[str] = None
    medium_settings: Optional[Dict[str, Any]] = None # For traditional art
    # For illustration styles
    line_work: Optional[str] = None
    coloring_technique: Optional[str] = None
    visual_style: Optional[str] = None
    # detail_level: Optional[str] = None # Covered in DetailSettings
    subject_treatment: Optional[str] = None

class LightingSettings(BaseModel):
    lighting_type: Optional[str] = None
    light_quality: Optional[str] = None
    light_direction: Optional[str] = None
    time_of_day: Optional[str] = None

class CompositionSettings(BaseModel):
    technique: Optional[str] = None
    focal_point: Optional[str] = None
    camera_angle: Optional[str] = None
    perspective: Optional[str] = None
    view_mode: Optional[str] = None
    color_interaction: Optional[str] = None
    motion_blur: Optional[str] = None
    # For logo styles
    key_elements_guidance: Optional[str] = None
    typography_guidance: Optional[str] = None
    # For cubism_mixed
    cubist_principles: Optional[str] = None
    # For phygital_hybrid
    physical_component: Optional[str] = None
    digital_component_AR: Optional[str] = None
    # For screen_printing_bold
    print_style_characteristics: Optional[str] = None
    # For mixed_media_journaling
    text_integration: Optional[str] = None
    # For digital_pixel_traditional
    integration_strategy: Optional[str] = None
    # For patchwork_fabric
    assembly_techniques_simulated: Optional[str] = None
    # For whimsical_fantasy
    narrative_style: Optional[str] = None
    # For anime_oilpainting
    character_design_approach: Optional[str] = None
    # For minimalist_geometric
    compositional_principles: Optional[str] = None
    # For pop_surrealism_ascii
    visual_irony_and_juxtaposition: Optional[str] = None
    # For dreamcore_weirdcore
    liminality_aspect: Optional[str] = None
    # For fantasy_battle
    environmental_context: Optional[str] = None # Also in EnvironmentSettings, clarify
    # For fantasy_landscape
    compositional_emphasis: Optional[str] = None
    # For cyberpunk_action
    environmental_interaction: Optional[str] = None
    # For cyberpunk_technology
    ui_ux_elements_focus: Optional[str] = None
    # For game_retro
    crt_simulation_effects: Optional[str] = None # Also in GameEngineSettings
    # For game_cel_shaded
    overall_aesthetic_goal: Optional[str] = None # Also in GameSettings

class ColorSettings(BaseModel):
    color_scheme: Optional[str] = None
    palette_type: Optional[str] = None
    color_temperature: Optional[str] = None
    color_contrast: Optional[str] = None
    dominant_colors: List[str] = Field(default_factory=list)
    # For logo styles
    color_palette_guidance: Optional[str] = None
    # For pop_surrealism_ascii
    color_interaction: Optional[str] = None # Also in CompositionSettings, clarify

class DetailSettings(BaseModel):
    detail_level: Optional[str] = None
    texture_quality: Optional[str] = None
    # For logo styles
    negative_prompt_suggestions: Optional[str] = None # This seems misplaced, more like a prompt generation aid

class EnvironmentSettings(BaseModel):
    weather: Optional[str] = None
    season: Optional[str] = None
    location_type: Optional[str] = None
    atmospheric_effects: List[str] = Field(default_factory=list)
    # For cyberpunk_technology
    environment_theme: Optional[str] = None # For sci_fi_settings too

class QualitySettings(BaseModel):
    resolution: Optional[str] = None
    rendering_quality: Optional[str] = None

# --- Specific Style Settings Models (Alphabetical for easier management) ---

class AbstractConceptualSettings(BaseModel): # From unique_style_templates
    visual_elements: List[str] = Field(default_factory=list)
    conceptual_approach: Optional[str] = None
    balance_type: Optional[str] = None
    movement_type: Optional[str] = None
    abstraction_level: Optional[str] = None
    composition_complexity: Optional[str] = None

class AbstractExpressionismCubismFusionSettings(BaseModel): # From hybrid_style_templates
    form_style: Optional[str] = None
    color_palette_dynamics: Optional[str] = None
    compositional_tension: Optional[str] = None
    emotional_intensity_focus: Optional[str] = None
    spatial_representation: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class AnimalInspiredSettings(BaseModel): # From unique_style_templates
    style_settings: Optional[Dict[str, Any]] = None # Contains art_movement
    composition_settings: Optional[Dict[str, Any]] = None # Contains technique
    color_settings: Optional[Dict[str, Any]] = None # Contains palette_type
    detail_settings: Optional[Dict[str, Any]] = None # Contains texture_quality
    base_template: Optional[Dict[str, Any]] = None # Contains aspect_ratio
    moods: List[str] = Field(default_factory=list)

class AnimeOilpaintingSettings(BaseModel): # From hybrid_style_templates
    character_design_approach: Optional[str] = None
    canvas_and_brushwork_simulation: Optional[str] = None
    lighting_and_shading_style: Optional[str] = None
    color_palette_fusion: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class ArtDecoRevivalSettings(BaseModel): # From unique_style_templates
    geometric_shapes: List[str] = Field(default_factory=list)
    ornate_details: List[str] = Field(default_factory=list)
    color_palette: List[str] = Field(default_factory=list)
    material_usage: List[str] = Field(default_factory=list)

class AsciiArtSettings(BaseModel): # From digital_style_templates
    character_set: Optional[str] = None
    font_style: Optional[str] = None
    character_resolution: Optional[str] = None
    contrast_method: Optional[str] = None
    color_depth: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class AugmentedRealityArtSettings(BaseModel): # From hybrid_style_templates
    media_components: Optional[str] = None
    interaction_methods: Optional[str] = None
    core_technology: Optional[str] = None
    tracking_and_mapping: Optional[str] = None
    user_interface_design: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class BiopunkSettings(BaseModel): # From unique_style_templates
    style_settings: Optional[Dict[str, Any]] = None
    composition_settings: Optional[Dict[str, Any]] = None
    color_settings: Optional[Dict[str, Any]] = None
    detail_settings: Optional[Dict[str, Any]] = None
    base_template: Optional[Dict[str, Any]] = None
    moods: List[str] = Field(default_factory=list)

class ClaymationSettings(BaseModel): # From hybrid_style_templates
    clay_type_simulation: Optional[str] = None
    surface_details: Optional[str] = None
    character_design_style: Optional[str] = None
    animation_style_emulation: Optional[str] = None
    set_and_prop_design: Optional[str] = None
    lighting_approach: Optional[str] = None
    color_palette_choice: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class CollageDigitalOverlaySettings(BaseModel): # From hybrid_style_templates
    physical_media_base: Optional[str] = None
    digital_overlay_techniques: Optional[str] = None
    integration_style: Optional[str] = None
    texture_play: Optional[str] = None
    narrative_or_theme: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class CubismMixedSettings(BaseModel): # From hybrid_style_templates
    cubist_principles: Optional[str] = None
    mixed_media_elements: Optional[str] = None
    textural_interplay: Optional[str] = None
    compositional_approach: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class CubismSettings(BaseModel): # From digital_style_templates (Digital Cubism)
    form_style: Optional[str] = None
    color_palette: Optional[str] = None
    composition: Optional[str] = None # Note: 'composition_settings' is top-level
    digital_techniques: List[str] = Field(default_factory=list)
    aesthetic_blend: Optional[str] = None

class CyberpunkActionSettings(BaseModel): # From hybrid_style_templates
    action_sequence_types: Optional[str] = None
    environmental_interaction: Optional[str] = None
    technological_and_fx_details: Optional[str] = None
    prevailing_atmosphere: Optional[str] = None
    motion_and_dynamics: Optional[str] = None

class CyberpunkTechSettings(BaseModel): # From hybrid_style_templates (Cyberpunk Technology Focus)
    specific_technology_examples: Optional[str] = None
    ui_ux_elements_focus: Optional[str] = None
    materiality_and_finish: Optional[str] = None
    lighting_on_technology: Optional[str] = None
    level_of_complexity: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class DigitalArtSettings(BaseModel): # From digital_style_templates (General Digital Art)
    software: Optional[str] = None
    rendering_technique: Optional[str] = None
    digital_effects: List[str] = Field(default_factory=list)
    resolution: Optional[str] = None
    filter_usage: List[str] = Field(default_factory=list)
    brush_type: Optional[str] = None
    layer_complexity: Optional[str] = None

class DigitalPaintingSettings(BaseModel): # From digital_style_templates
    platform: Optional[str] = None
    brushwork: Optional[str] = None
    canvas_texture_simulation: Optional[str] = None
    layering_techniques: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class DigitalPixelTraditionalSettings(BaseModel): # From hybrid_style_templates
    pixel_art_component: Optional[str] = None
    traditional_painting_component: Optional[str] = None
    integration_strategy: Optional[str] = None
    thematic_purpose: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class DreamcoreWeirdcoreSettings(BaseModel): # From hybrid_style_templates
    dominant_atmosphere: Optional[str] = None
    visual_distortion_techniques: Optional[str] = None
    common_motifs_and_iconography: Optional[str] = None
    liminality_aspect: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class ExperimentalMixedMediaSettings(BaseModel): # From hybrid_style_templates
    physical_materials: Optional[str] = None
    digital_processes: Optional[str] = None
    core_techniques: Optional[str] = None
    conceptual_focus: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class FantasyBattleSettings(BaseModel): # From hybrid_style_templates
    combatant_types: Optional[str] = None
    # environmental_context: Optional[str] = None # Already in top-level EnvironmentSettings
    action_and_impact_elements: Optional[str] = None
    overall_atmosphere: Optional[str] = None
    magical_special_effects: Optional[str] = None
    lighting_dynamics: Optional[str] = None
    compositional_strategy: Optional[str] = None

class FantasyCityscapeSettings(BaseModel): # From hybrid_style_templates
    architecture_styles_envisioned: Optional[str] = None
    environmental_context_details: Optional[str] = None
    key_magical_elements: Optional[str] = None
    time_of_day_and_atmosphere: Optional[str] = None
    sense_of_scale_and_wonder: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class FantasyLandscapeSettings(BaseModel): # From hybrid_style_templates
    geographical_features: Optional[str] = None
    architectural_elements: Optional[str] = None
    magical_phenomena: Optional[str] = None
    overall_atmosphere: Optional[str] = None
    lighting_and_sky_details: Optional[str] = None
    color_palette_mood: Optional[str] = None
    # compositional_emphasis: Optional[str] = None # Already in top-level CompositionSettings

class FantasySettings(BaseModel): # From unique_style_templates (General Fantasy)
    world_building: Optional[str] = None
    technological_level: Optional[str] = None
    reality_distortion: Optional[str] = None
    atmosphere: Optional[str] = None # Can conflict with EnvironmentSettings.atmospheric_effects

class FerrofluidSettings(BaseModel): # From unique_style_templates
    style_settings: Optional[Dict[str, Any]] = None
    composition_settings: Optional[Dict[str, Any]] = None
    color_settings: Optional[Dict[str, Any]] = None
    detail_settings: Optional[Dict[str, Any]] = None
    base_template: Optional[Dict[str, Any]] = None
    moods: List[str] = Field(default_factory=list)

class FractalArtSettings(BaseModel): # From digital_style_templates
    software: Optional[str] = None
    fractal_type: Optional[str] = None
    coloring_techniques: Optional[str] = None
    rendering_parameters: Optional[str] = None
    mathematical_basis: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class GameEngineSettings(BaseModel): # For game_style, game_retro, game_cel_shaded
    engine_type: Optional[str] = None
    render_quality: Optional[str] = None
    shader_type: Optional[str] = None
    special_effects: List[str] = Field(default_factory=list)
    post_effects: List[str] = Field(default_factory=list)
    resolution: Optional[str] = None
    physics_settings: List[str] = Field(default_factory=list)
    animation_style: Optional[str] = None
    simulated_engine_type: Optional[str] = None
    rendering_characteristics: Optional[str] = None
    sprite_and_tile_animation: Optional[str] = None
    crt_simulation_effects: Optional[str] = None
    color_palette_management: Optional[str] = None
    resolution_handling: Optional[str] = None
    simulated_engine_pipeline: Optional[str] = None
    shading_model: Optional[str] = None
    outline_method: Optional[str] = None
    special_effects_rendering: Optional[str] = None
    post_processing_stack: Optional[str] = None
    target_resolution_and_aa: Optional[str] = None

class GameSettings(BaseModel): # For game_style, game_retro, game_cel_shaded
    interactivity: Optional[str] = None
    environment_type: Optional[str] = None
    character_style: Optional[str] = None
    # lighting_type: Optional[str] = None # In top-level LightingSettings
    target_retro_style: Optional[str] = None
    emulated_color_depth: Optional[str] = None
    animation_techniques: Optional[str] = None
    character_and_animation_style: Optional[str] = None
    lighting_philosophy: Optional[str] = None
    overall_aesthetic_goal: Optional[str] = None

class GenerativeArtSettings(BaseModel): # From digital_style_templates
    algorithm_type: Optional[str] = None
    software_tools: Optional[str] = None
    visual_complexity: Optional[str] = None
    artist_control: Optional[str] = None
    output_forms: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class GlitchArtSettings(BaseModel): # From digital_style_templates
    glitch_techniques: List[str] = Field(default_factory=list)
    corruption_level: Optional[str] = None
    artifacts: List[str] = Field(default_factory=list)
    base_image: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class HybridTraditionalDigitalSettings(BaseModel): # From hybrid_style_templates
    media_fusion: Optional[str] = None
    traditional_elements_emphasis: Optional[str] = None
    digital_enhancements: List[str] = Field(default_factory=list)
    workflow_implication: Optional[str] = None
    aesthetic_goal: Optional[str] = None
    digital_tools_suite: Optional[str] = None

class InstallationArtSettings(BaseModel): # From hybrid_style_templates
    media_components: Optional[str] = None
    scale_and_space: Optional[str] = None
    interactivity_type: Optional[str] = None
    spatial_arrangement_logic: Optional[str] = None
    technology_integration_tools: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class IsometricSettings(BaseModel): # From digital_style_templates
    view_angle: Optional[str] = None
    object_arrangement: Optional[str] = None
    # color_palette: Optional[str] = None # In top-level ColorSettings
    # detail_level: Optional[str] = None # In top-level DetailSettings

class KineticArtSettings(BaseModel): # From unique_style_templates
    style_settings: Optional[Dict[str, Any]] = None
    composition_settings: Optional[Dict[str, Any]] = None
    color_settings: Optional[Dict[str, Any]] = None
    detail_settings: Optional[Dict[str, Any]] = None
    base_template: Optional[Dict[str, Any]] = None
    moods: List[str] = Field(default_factory=list)

class KineticAsciiSettings(BaseModel): # From hybrid_style_templates
    motion_type: Optional[str] = None
    character_set: Optional[str] = None
    visual_flow: Optional[str] = None
    energy_motif: Optional[str] = None
    articulation: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class MaterialSculpturalSettings(BaseModel): # From unique_style_templates
    primary_material: Optional[str] = None
    technique: Optional[str] = None # Also top-level
    surface_quality: Optional[str] = None
    form_type: Optional[str] = None
    dimensionality: Optional[str] = None
    scale: Optional[str] = None
    finishing: Optional[str] = None

class MediterraneanStyleSettings(BaseModel): # From hybrid_style_templates
    key_environments: Optional[str] = None
    color_palette_emphasis: Optional[str] = None
    lighting_characteristics: Optional[str] = None
    digital_painting_techniques: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class MinimalistGeometricSettings(BaseModel): # From hybrid_style_templates
    geometric_primitives: Optional[str] = None
    compositional_principles: Optional[str] = None
    color_usage: Optional[str] = None
    line_quality: Optional[str] = None
    digital_execution_emphasis: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class MinimalistSettings(BaseModel): # From digital_style_templates
    simplicity_level: Optional[str] = None
    geometric_elements: List[str] = Field(default_factory=list)
    negative_space: Optional[str] = None
    line_type: Optional[str] = None
    color_count: Optional[str] = None
    composition_balance: Optional[str] = None

class MixedMediaCollageSettings(BaseModel): # From hybrid_style_templates (Physical Mixed Media Collage)
    physical_materials_palette: List[str] = Field(default_factory=list)
    assembly_methods_simulated: Optional[str] = None
    textural_emphasis: Optional[str] = None
    dimensional_aspects: Optional[str] = None
    conceptual_approach: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class MixedMediaJournalingSettings(BaseModel): # From hybrid_style_templates
    common_media: List[str] = Field(default_factory=list)
    layering_style: Optional[str] = None
    # text_integration: Optional[str] = None # In top-level CompositionSettings
    textural_qualities: Optional[str] = None
    expressive_marks: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class MorphismSurrealSettings(BaseModel): # From hybrid_style_templates
    transformation_style_details: Optional[str] = None
    morphing_dynamics_and_flow: Optional[str] = None
    conceptual_underpinnings: Optional[str] = None
    color_and_texture_in_morphing: Optional[str] = None
    compositional_focus: Optional[str] = None # Also top-level
    aesthetic_blend: Optional[str] = None

class NightcoreSettings(BaseModel): # From unique_style_templates
    style_settings: Optional[Dict[str, Any]] = None
    composition_settings: Optional[Dict[str, Any]] = None
    color_settings: Optional[Dict[str, Any]] = None
    post_processing: List[str] = Field(default_factory=list) # Also top-level
    base_template: Optional[Dict[str, Any]] = None
    moods: List[str] = Field(default_factory=list)

class OpticArtSettings(BaseModel): # From unique_style_templates
    style_settings: Optional[Dict[str, Any]] = None
    composition_settings: Optional[Dict[str, Any]] = None
    color_settings: Optional[Dict[str, Any]] = None
    detail_settings: Optional[Dict[str, Any]] = None
    base_template: Optional[Dict[str, Any]] = None
    moods: List[str] = Field(default_factory=list)

class PaperQuillingSettings(BaseModel): # From hybrid_style_templates
    coil_and_shape_types: Optional[str] = None
    paper_strip_characteristics: Optional[str] = None
    pattern_density_and_style: Optional[str] = None
    dimensionality_focus: Optional[str] = None
    construction_details: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PapercraftSettings(BaseModel): # From digital_style_templates
    layering_technique: Optional[str] = None
    paper_type: Optional[str] = None
    edge_quality: Optional[str] = None
    construction_method: Optional[str] = None
    motif: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PatchworkCollageSettings(BaseModel): # From hybrid_style_templates
    material_simulation: Optional[str] = None
    assembly_techniques: Optional[str] = None
    texture_emphasis_details: Optional[str] = None
    color_and_pattern_logic: Optional[str] = None
    pattern_and_motif_types: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PatchworkFabricSettings(BaseModel): # From hybrid_style_templates
    fabric_types_simulated: Optional[str] = None
    # assembly_techniques_simulated: Optional[str] = None # In top-level CompositionSettings
    textural_details: Optional[str] = None
    color_and_pattern_choices: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PhygitalHybridSettings(BaseModel): # From hybrid_style_templates
    # physical_component: Optional[str] = None # In top-level CompositionSettings
    # digital_component_AR: Optional[str] = None # In top-level CompositionSettings
    media_fusion_concept: Optional[str] = None
    technology_stack: Optional[str] = None
    interaction_modalities: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PhotorealismGlitchSettings(BaseModel): # From hybrid_style_templates
    glitch_intensity: Optional[str] = None
    glitch_types_simulated: List[str] = Field(default_factory=list)
    base_image_clarity: Optional[str] = None
    conceptual_theme: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PixelArtSettings(BaseModel): # From digital_style_templates
    resolution: Optional[str] = None
    color_count: Optional[str] = None
    pixel_technique: Optional[str] = None
    shading_method: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PixelPatchworkSettings(BaseModel): # From hybrid_style_templates
    art_style_fusion: Optional[str] = None
    color_palette_constraints: Optional[str] = None
    textural_qualities: Optional[str] = None
    compositional_structure: Optional[str] = None
    dimensional_play: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PopSurrealismAsciiSettings(BaseModel): # From hybrid_style_templates
    pop_surrealist_subject_matter: Optional[str] = None
    ascii_rendering_technique: Optional[str] = None
    # visual_irony_and_juxtaposition: Optional[str] = None # In top-level CompositionSettings
    # color_interaction: Optional[str] = None # In top-level ColorSettings
    pattern_and_density: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class PsychedelicSettings(BaseModel): # From unique_style_templates
    color_palette: Optional[str] = None
    patterns: Optional[str] = None
    visual_effects: List[str] = Field(default_factory=list)
    mood: Optional[str] = None # moods is top-level

class SciFiFuturisticSettings(BaseModel): # From hybrid_style_templates
    core_technology_themes: Optional[str] = None
    environment_archetypes: Optional[str] = None
    lighting_and_atmosphere_details: Optional[str] = None
    color_palette_emphasis: Optional[str] = None
    key_visual_elements: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class SciFiSettings(BaseModel): # From digital_style_templates
    technology_level: Optional[str] = None
    # environment_theme: Optional[str] = None # In top-level EnvironmentSettings
    lighting_style: Optional[str] = None # In top-level LightingSettings
    # color_palette: Optional[str] = None # In top-level ColorSettings
    visual_elements: List[str] = Field(default_factory=list)
    aesthetic_blend: Optional[str] = None

class ScientificTechnologicalHybridSettings(BaseModel): # From hybrid_style_templates
    media_and_tools: Optional[str] = None
    conceptual_basis: Optional[str] = None
    technology_involved: Optional[str] = None
    data_visualization_techniques: Optional[str] = None
    interactivity_options: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class ScreenPrintingBoldSettings(BaseModel): # From hybrid_style_templates
    # print_style_characteristics: Optional[str] = None # In top-level CompositionSettings
    color_palette_details: Optional[str] = None
    ink_and_texture_properties: Optional[str] = None
    ink_properties: Optional[str] = None
    design_elements: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class SteampunkSettings(BaseModel): # From digital_style_templates
    technology_style: Optional[str] = None
    materials: List[str] = Field(default_factory=list)
    mechanical_elements: List[str] = Field(default_factory=list)
    # color_palette: Optional[str] = None # In top-level ColorSettings
    aesthetic_blend: Optional[str] = None

class SurrealismSettings(BaseModel): # From digital_style_templates (Digital Surrealism)
    conceptual_approach: Optional[str] = None
    # color_scheme: Optional[str] = None # In top-level ColorSettings
    composition: Optional[str] = None # In top-level CompositionSettings
    mood: Optional[str] = None # moods is top-level
    digital_techniques: List[str] = Field(default_factory=list)

class TradigitalMixedMediaSettings(BaseModel): # From hybrid_style_templates (Acrylic Base)
    media_fusion_process: Optional[str] = None
    acrylic_characteristics_preserved: Optional[str] = None
    digital_enhancement_techniques: Optional[str] = None
    texture_interaction: Optional[str] = None
    color_palette_synergy: Optional[str] = None
    digital_tools_employed: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class TraditionalPaintingDrawingSettings(BaseModel): # From unique_style_templates
    painting_medium: Optional[str] = None
    support_type: Optional[str] = None
    # technique: Optional[str] = None # In top-level CompositionSettings
    texture: Optional[str] = None # In top-level DetailSettings
    layering_technique: Optional[str] = None
    stroke_style: Optional[str] = None
    detail_approach: Optional[str] = None

class VaporwaveSettings(BaseModel): # From digital_style_templates
    nostalgic_elements: List[str] = Field(default_factory=list)
    digital_effects: List[str] = Field(default_factory=list)
    typography: Optional[str] = None
    aesthetic_blend: Optional[str] = None

class VectorSettings(BaseModel): # From digital_style_templates
    software: Optional[str] = None
    line_quality: Optional[str] = None
    fill_type: Optional[str] = None
    design_elements: List[str] = Field(default_factory=list)
    aesthetic_blend: Optional[str] = None

class WhimsicalFantasySettings(BaseModel): # From hybrid_style_templates
    character_archetypes: Optional[str] = None
    common_motifs: Optional[str] = None
    textural_approach: Optional[str] = None
    emotional_tone: Optional[str] = None
    # narrative_style: Optional[str] = None # In top-level CompositionSettings
    aesthetic_blend: Optional[str] = None

class WhimsicalMixedMediaSettings(BaseModel): # From hybrid_style_templates
    core_motifs: List[str] = Field(default_factory=list)
    material_palette: Optional[str] = None
    technique_emphasis: Optional[str] = None
    overall_feeling: Optional[str] = None
    aesthetic_blend: Optional[str] = None

# --- 3D Specific Settings Models ---
class SoftwareSettings3D(BaseModel):
    suite: Optional[str] = None
    renderer: Optional[str] = None
    version: Optional[str] = None

class RenderSettings3D(BaseModel):
    polycount: Optional[str] = None
    sampling: Optional[str] = None
    denoiser: Optional[Union[bool, str]] = None
    resolution: Optional[str] = None
    aspect_ratio: Optional[str] = None
    frame_number: Optional[Union[int, str]] = None

class LightingSetup3D(BaseModel):
    system: Optional[str] = None
    intensity: Optional[Union[float, str]] = None
    color: Optional[str] = None
    shadows: Optional[str] = None

class MaterialSettings3D(BaseModel):
    shader_type: Optional[str] = None
    subsurface_scattering: Optional[Union[float, str]] = None
    texture_maps: List[str] = Field(default_factory=list)
    bump_map: Optional[str] = None
    displacement: Optional[str] = None
    wireframe_options: Optional[Dict[str, Any]] = None
    background_options: Optional[Dict[str, Any]] = None
    material_properties: Optional[Dict[str, Any]] = None
    ambient_occlusion: Optional[Dict[str, Any]] = None
    outlines_settings: Optional[Dict[str, Any]] = None
    hair_shader_specifics: Optional[Dict[str, Any]] = None

# --- Main ImagenSettings Model ---
class ImagenSettings(BaseModel):
    # Common settings groups
    style_settings: StyleSettings = Field(default_factory=StyleSettings)
    lighting_settings: LightingSettings = Field(default_factory=LightingSettings)
    composition_settings: CompositionSettings = Field(default_factory=CompositionSettings)
    color_settings: ColorSettings = Field(default_factory=ColorSettings)
    detail_settings: DetailSettings = Field(default_factory=DetailSettings)
    environment_settings: EnvironmentSettings = Field(default_factory=EnvironmentSettings)
    quality_settings: QualitySettings = Field(default_factory=QualitySettings)
    camera_settings: Optional[CameraSettings] = None

    # Specific style groups (alphabetical)
    abstract_conceptual_settings: Optional[AbstractConceptualSettings] = None
    abstract_expressionism_cubism_fusion_settings: Optional[AbstractExpressionismCubismFusionSettings] = None
    animal_inspired_settings: Optional[AnimalInspiredSettings] = None
    anime_oilpainting_settings: Optional[AnimeOilpaintingSettings] = None
    art_deco_revival_settings: Optional[ArtDecoRevivalSettings] = None
    ascii_art_settings: Optional[AsciiArtSettings] = None
    augmented_reality_art_settings: Optional[AugmentedRealityArtSettings] = None
    biopunk_settings: Optional[BiopunkSettings] = None
    claymation_settings: Optional[ClaymationSettings] = None
    collage_digital_overlay_settings: Optional[CollageDigitalOverlaySettings] = None
    cubism_mixed_settings: Optional[CubismMixedSettings] = None
    cubism_settings: Optional[CubismSettings] = None # Digital Cubism
    cyberpunk_action_settings: Optional[CyberpunkActionSettings] = None
    cyberpunk_tech_settings: Optional[CyberpunkTechSettings] = None # Cyberpunk Technology Focus
    digital_art_settings: Optional[DigitalArtSettings] = None # General Digital Art
    digital_painting_settings: Optional[DigitalPaintingSettings] = None
    digital_pixel_traditional_settings: Optional[DigitalPixelTraditionalSettings] = None
    dreamcore_weirdcore_settings: Optional[DreamcoreWeirdcoreSettings] = None
    experimental_mixed_media_settings: Optional[ExperimentalMixedMediaSettings] = None
    fantasy_battle_settings: Optional[FantasyBattleSettings] = None
    fantasy_cityscape_settings: Optional[FantasyCityscapeSettings] = None
    fantasy_landscape_settings: Optional[FantasyLandscapeSettings] = None
    fantasy_settings: Optional[FantasySettings] = None # General Fantasy
    ferrofluid_settings: Optional[FerrofluidSettings] = None
    fractal_art_settings: Optional[FractalArtSettings] = None
    game_engine_settings: Optional[GameEngineSettings] = None
    game_settings: Optional[GameSettings] = None
    generative_art_settings: Optional[GenerativeArtSettings] = None
    glitch_art_settings: Optional[GlitchArtSettings] = None
    hybrid_traditional_digital_settings: Optional[HybridTraditionalDigitalSettings] = None
    installation_art_settings: Optional[InstallationArtSettings] = None
    isometric_settings: Optional[IsometricSettings] = None # Digital Isometric
    kinetic_art_settings: Optional[KineticArtSettings] = None
    kinetic_ascii_settings: Optional[KineticAsciiSettings] = None
    material_sculptural_settings: Optional[MaterialSculpturalSettings] = None
    mediterranean_style_settings: Optional[MediterraneanStyleSettings] = None
    minimalist_geometric_settings: Optional[MinimalistGeometricSettings] = None
    minimalist_settings: Optional[MinimalistSettings] = None # Digital Minimalist
    mixed_media_collage_settings: Optional[MixedMediaCollageSettings] = None # Physical
    mixed_media_journaling_settings: Optional[MixedMediaJournalingSettings] = None
    morphism_surreal_settings: Optional[MorphismSurrealSettings] = None
    nightcore_settings: Optional[NightcoreSettings] = None
    optic_art_settings: Optional[OpticArtSettings] = None
    paper_quilling_settings: Optional[PaperQuillingSettings] = None
    papercraft_settings: Optional[PapercraftSettings] = None # Digital Papercraft
    patchwork_collage_settings: Optional[PatchworkCollageSettings] = None
    patchwork_fabric_settings: Optional[PatchworkFabricSettings] = None
    phygital_hybrid_settings: Optional[PhygitalHybridSettings] = None
    photorealism_glitch_settings: Optional[PhotorealismGlitchSettings] = None
    pixel_art_settings: Optional[PixelArtSettings] = None # Digital Pixel Art
    pixel_patchwork_settings: Optional[PixelPatchworkSettings] = None
    pop_surrealism_ascii_settings: Optional[PopSurrealismAsciiSettings] = None
    psychedelic_settings: Optional[PsychedelicSettings] = None
    sci_fi_futuristic_settings: Optional[SciFiFuturisticSettings] = None
    sci_fi_settings: Optional[SciFiSettings] = None # Digital Sci-Fi
    scientific_technological_hybrid_settings: Optional[ScientificTechnologicalHybridSettings] = None
    screen_printing_bold_settings: Optional[ScreenPrintingBoldSettings] = None
    steampunk_settings: Optional[SteampunkSettings] = None # Digital Steampunk
    surrealism_settings: Optional[SurrealismSettings] = None # Digital Surrealism
    tradigital_mixed_media_settings: Optional[TradigitalMixedMediaSettings] = None # Acrylic Base
    traditional_painting_drawing_settings: Optional[TraditionalPaintingDrawingSettings] = None
    vaporwave_settings: Optional[VaporwaveSettings] = None
    vector_settings: Optional[VectorSettings] = None # Digital Vector Art
    whimsical_fantasy_settings: Optional[WhimsicalFantasySettings] = None
    whimsical_mixed_media_settings: Optional[WhimsicalMixedMediaSettings] = None

    # 3D specific settings groups (using renamed models)
    software_settings_3d: Optional[SoftwareSettings3D] = Field(default=None, alias="software_settings") # Alias for backward compatibility if old templates use "software_settings"
    render_settings_3d: Optional[RenderSettings3D] = Field(default=None, alias="render_settings")
    lighting_setup_3d: Optional[LightingSetup3D] = Field(default=None, alias="lighting_setup")
    material_settings_3d: Optional[MaterialSettings3D] = Field(default=None, alias="material_settings")

    # For portrait styles that have specific nested dicts (already in StyleSettings or handled by specific models if complex enough)
    futuristic_elements: Optional[Dict[str, Any]] = None
    illustration_specifics: Optional[Dict[str, Any]] = None
    pop_art_elements: Optional[Dict[str, Any]] = None
    environmental_context: Optional[Dict[str, Any]] = None
    caricature_elements: Optional[Dict[str, Any]] = None
    conceptual_elements: Optional[Dict[str, Any]] = None
    fashion_shoot_elements: Optional[Dict[str, Any]] = None
    selfie_characteristics: Optional[Dict[str, Any]] = None
    other_portrait_specifics: Optional[Dict[str, Any]] = None
    
    # For logo styles (these are more about guiding prompt generation for Imagen3)
    ai_prompt_focus: Optional[str] = None
    logo_style_description: Optional[str] = None
    # key_elements_guidance: Optional[str] = None # Moved to CompositionSettings
    # color_palette_guidance: Optional[str] = None # Moved to ColorSettings
    # typography_guidance: Optional[str] = None # Moved to CompositionSettings
    # negative_prompt_suggestions: Optional[str] = None # Moved to DetailSettings
    imagen3_prompt_structure: Optional[str] = None


    negative_prompt: str = "low quality, blurry, jpeg artifacts"
    style_negative_prompt: str = "clashing styles, bad composition"

    class Config:
        extra = 'allow' # Allow other fields not explicitly defined, useful during development
        populate_by_name = True # Allows using alias for population

class AIPreset(BaseModel):
    preset_name: str
    moods: List[str] = Field(default_factory=list)
    aspect_ratio: str = "16:9"
    description: str = ""
    styles: List[str] = Field(default_factory=list)
    imagen_settings: ImagenSettings = Field(default_factory=ImagenSettings)

    @validator('styles', pre=True, always=True)
    def ensure_styles_is_list(cls, v):
        if isinstance(v, str):
            return [v]
        if v is None: # Handle case where styles might be None
            return []
        return v