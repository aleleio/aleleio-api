import os
import yaml

from src.start import ROOT


def get_project_version(project):
    """Get the current version from openapi.yml config file.
    """
    match project:
        case "aleleio-api":
            yml_path = ROOT.joinpath('openapi.yml')
            with open(yml_path, 'r') as fin:
                yml = yaml.safe_load(fin)
            return yml['info']['version']
        case "aleleio-web":
            return "0.0.0"
        case "teambuilding-games":
            return "0.0.0"


