from pathlib import Path
import tomllib

from .models import ModelProfile, ModelProfileName

MODEL_PROFILES: tuple[ModelProfileName, ...] = ("fast", "general")


def load_model_profiles(config_path: Path) -> dict[ModelProfileName, ModelProfile]:
    if not config_path.is_file():
        raise ValueError(f"missing model profile configuration: {config_path}")
    with config_path.open("rb") as profile_file:
        data = tomllib.load(profile_file)

    profiles: dict[ModelProfileName, ModelProfile] = {}
    for profile_name in MODEL_PROFILES:
        profile_data = data.get(profile_name)
        if not isinstance(profile_data, dict):
            raise ValueError(f"missing model profile: {profile_name}")
        model = profile_data.get("model")
        if not isinstance(model, str) or not model.strip():
            raise ValueError(
                f"{profile_name} model profile must declare a nonblank model"
            )
        profiles[profile_name] = ModelProfile(
            model_profile=profile_name,
            model=model,
        )
    return profiles
