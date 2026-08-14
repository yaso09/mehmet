"""YAML loader for GitHub Actions workflows.

GitHub Actions uses YAML 1.2, where `on` is a plain string key.
PyYAML's default SafeLoader follows YAML 1.1 and would turn `on:` into a
boolean, so we strip the implicit bool resolver for workflow files.
"""

import yaml


def load_github_workflow(path):
    class GitHubActionsLoader(yaml.SafeLoader):
        pass

    GitHubActionsLoader.yaml_implicit_resolvers = {
        key: [
            resolver
            for resolver in resolvers
            if resolver[0] != "tag:yaml.org,2002:bool"
        ]
        for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }

    with open(path, encoding="utf-8") as f:
        return yaml.load(f, Loader=GitHubActionsLoader)
