"""
Master URL List for UEFN RAG Assistant
=======================================
This file is the single source of truth for all URLs to scrape.

Update cadence:
- Content updates: Fully automatic (weekly Lambda scrape)
- New pages: Add URLs manually to appropriate section below
- Patch notes: Semi-automatic via discover_patch_notes()

Last updated: March 2026
"""

# ============================================================
# SECTION 1: VERSE LANGUAGE REFERENCE
# ============================================================
VERSE_LANGUAGE_URLS = [
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-language-reference",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-language-version-updates-and-deprecations-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/expressions-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/functions-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/constants-and-variables-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/common-types-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/composite-types-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/container-types-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/control-flow-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/operators-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/modules-and-paths-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/specifiers-and-attributes-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/failure-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/time-flow-and-concurrency-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/working-with-types-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/grouping-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/code-blocks-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/comments-in-verse",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-glossary",
]

# ============================================================
# SECTION 2: TUTORIALS & WORKFLOWS
# ============================================================
TUTORIAL_URLS = [
    "https://dev.epicgames.com/documentation/en-us/fortnite/programming-with-verse-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/onboarding-guide-to-programming-with-verse-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/build-a-game-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/learn-game-mechanics-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/using-devices-in-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/ingame-user-interfaces-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/ai-and-npcs-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/animation-and-cinematics-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/environments-and-landscapes-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/lighting-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/materials-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/audio-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/visual-effects-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/import-content-and-islands-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/collaborate-and-publish-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/editor-best-practices-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/island-settings-in-uefn-and-fortnite-creative",
    "https://dev.epicgames.com/documentation/en-us/fortnite/scene-graph-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/modeling-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/physics",
]

# ============================================================
# SECTION 3: TROUBLESHOOTING & OPTIMIZATION
# ============================================================
TROUBLESHOOTING_URLS = [
    "https://dev.epicgames.com/documentation/en-us/fortnite/memory-and-optimization-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/getting-to-know-the-user-interface-in-unreal-editor-for-fortnite",
]

# ============================================================
# SECTION 4: PATCH NOTES
# Add new patch note URLs here as Epic releases updates
# Pattern: .../XX-XX-fortnite-ecosystem-updates-and-release-notes
# ============================================================
PATCH_NOTE_URLS = [
    "https://dev.epicgames.com/documentation/en-us/fortnite/whats-new-in-unreal-editor-for-fortnite",
    "https://dev.epicgames.com/documentation/en-us/fortnite/39-50-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/39-40-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/39-30-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/39-20-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/39-10-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/39-00-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/38-10-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/38-00-fortnite-ecosystem-updates-and-release-notes",
    "https://dev.epicgames.com/documentation/en-us/fortnite/37-00-fortnite-ecosystem-updates-and-release-notes",
]

# ============================================================
# SECTION 5: VERSE API REFERENCE
# Manually curated high-value API pages
# ============================================================
VERSE_API_URLS = [
    # Characters
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/characters/fort_character",
    # Devices - Core
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/creative_device",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/creative_prop",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/creative_object",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/prop_spawner_base_device",
    # Devices - AI
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/accolades_device",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/devices/ai_patrol_path_device",
    # Devices - Full List 
    
    # Playspaces
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/playspaces/fort_playspace",
    # Game
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/game/damageable",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/game/fort_round_manager",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/game/healable",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/game/healthful",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/game/positional",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/game/shieldable",
    # UI
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ui",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ui/fort_hud_controller",
    # AI
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/npc_behavior",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/guard_actions_component",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/guard_awareness_component",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/npc_actions_component",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/npc_awareness_component",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/npc_target_info",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/focus_interface",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/fort_leashable",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/navigatable",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/ai/equipped_sidekick_component",
    # Teams
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/teams/fort_team_collection",
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/teams/team_attitude",
    # Itemization
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/itemization/fort_inventory_component",
    # Animation
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/fortnitedotcom/animation/playanimation",
    # Verse.org - Simulation (core player/game objects)
    "https://dev.epicgames.com/documentation/en-us/fortnite/verse-api/versedotorg/simulation/player",
]


# ============================================================
# MASTER URL BUILDER
# ============================================================
def get_all_urls():
    """
    Returns the complete deduplicated master URL list
    organized by category.
    """

    all_urls = {
        "verse-language": VERSE_LANGUAGE_URLS,
        "tutorial": TUTORIAL_URLS,
        "troubleshooting": TROUBLESHOOTING_URLS,
        "patch-notes": PATCH_NOTE_URLS,
        "api-reference": VERSE_API_URLS,
    }

    # Deduplicate across all categories
    seen = set()
    deduplicated = {}
    for category, urls in all_urls.items():
        unique = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique.append(url)
        deduplicated[category] = unique

    return deduplicated

def print_summary():
    """Print a summary of all URLs in the master list."""
    all_urls = get_all_urls()
    total = sum(len(urls) for urls in all_urls.values())

    print("=== MASTER URL LIST SUMMARY ===")
    print(f"Total URLs: {total}")
    for category, urls in all_urls.items():
        print(f"  {category}: {len(urls)} pages")

if __name__ == "__main__":
    print_summary()