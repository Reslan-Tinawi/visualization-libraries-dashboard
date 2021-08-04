import pandas as pd
from github import Github
from repo import Repo

repos_dict = {
    "altair": "altair-viz/altair",
    "bokeh": "bokeh/bokeh",
    "chartify": "spotify/chartify",
    "diagram": "tehmaze/diagram",
    "ggpy": "yhat/ggpy",
    "glumpy": "glumpy/glumpy",
    "holoviews": "holoviz/holoviews",
    "mayavi": "enthought/mayavi",
    "matplotlib": "matplotlib/matplotlib",
    "missingo": "ResidentMario/missingno",
    "plotly": "plotly/plotly.py",
    "pyqtgraph": "pyqtgraph/pyqtgraph",
    "pyvista": "pyvista/pyvista",
    "seaborn": "mwaskom/seaborn",
    "toyplot": "sandialabs/toyplot",
    "three": "stemkoski/three.py",
    "veusz": "veusz/veusz",
    "vispy": "vispy/vispy",
}

data_path = './data/raw/'


def init():
    token = ""
    gh_client = Github(token)
    repos_list = []

    for repo_name, repo_full_name in repos_dict.items():
        repos_list.append(
            Repo(name=repo_name, full_name=repo_full_name, gh_client=gh_client)
        )
    return repos_list


def create_repos_feature(repos_list):
    repos_features = pd.concat(
        [repo.get_repo_features() for repo in repos_list]
    ).reset_index()
    print(f'getting repos_features finished with shape {repos_features.shape}')
    repos_features.to_csv(data_path + 'repos_features.csv', index=False)


def create_contrib_features(repos_list):
    contrib_features = pd.concat(
        [repo.get_contrib_features() for repo in repos_list]
    ).reset_index()
    print(
        f'getting contrib_features finished with shape {contrib_features.shape}')
    contrib_features.to_csv(data_path + 'contrib_features.csv', index=False)


def create_repo_releases(repos_list):
    repo_releases = pd.concat(
        [repo.get_repo_releases() for repo in repos_list]
    ).reset_index()
    print(f'getting repo_releases finished with shape {repo_releases.shape}')
    repo_releases.to_csv(data_path + 'repo_releases.csv', index=False)


def create_stars_history(repos_list):
    stars_history = pd.concat(
        [repo.get_stars_history() for repo in repos_list]
    ).reset_index()
    print(f'getting stars_history finished with shape {stars_history.shape}')
    stars_history.to_csv(data_path + 'stars_history.csv', index=False)


def create_repo_issues(repos_list):
    repo_issues = pd.concat(
        [repo.get_repo_issues() for repo in repos_list]
    ).reset_index()
    print(f'getting repo_issues finished with shape {repo_issues.shape}')
    repo_issues.to_csv(data_path + 'repo_issues.csv', index=False)


def create_repo_pull_requests(repos_list):
    repo_pull_requests = pd.concat(
        [repo.get_repo_pull_requests() for repo in repos_list]
    ).reset_index()
    print(
        f'getting repo_pull_requests finished with shape {repo_pull_requests.shape}')
    repo_pull_requests.to_csv(
        data_path + 'repo_pull_requests.csv', index=False)


if __name__ == '__main__':
    print('Getting data from github repositories')
    print('initializing.... ')
    repos_list = init()
    create_repos_feature(repos_list)
    create_contrib_features(repos_list)
    create_repo_releases(repos_list)
    create_stars_history(repos_list)
    create_repo_issues(repos_list)
    create_repo_pull_requests(repos_list)
